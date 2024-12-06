from dataclasses import asdict, dataclass, field
from pathlib import Path
import pickle
from typing import Optional, Union

import pandas as pd
import yaml

from annotation_tool import common


@dataclass(frozen=True, eq=True)
class Config:
    previous_project: Optional[Path] = None
    font_size: int = 10
    keep_aspectratio: bool = False
    autosave_interval_sec: int = 30
    indexing_timeout_sec: int = 5
    group_class_separator: str = common.GROUP_CLASS_SEPARATOR

    def to_disk(self, path):
        data = asdict(self)
        if data["previous_project"] is not None:
            data["previous_project"] = data["previous_project"].as_posix()
        with open(path, "w") as file:
            yaml.dump(data, file)

    @staticmethod
    def from_disk(path):
        with open(path, "r") as file:
            data = yaml.safe_load(file)
            if data["previous_project"] is not None:
                data["previous_project"] = Path(data["previous_project"])
            return Config(**data)

    def update_project(self, project: Optional[Path]) -> "Config":
        return Config(
            project,
            self.font_size,
            self.keep_aspectratio,
            self.autosave_interval_sec,
            self.indexing_timeout_sec,
            self.group_class_separator,
        )


@dataclass(frozen=True, eq=True)
class AnnotationGroup:
    name: str
    classes: list[str]
    exclusive: bool

    def rename(self, new_name: str) -> "AnnotationGroup":
        return AnnotationGroup(new_name, self.classes, self.exclusive)

    def set_exclusive(self, exclusive: bool) -> "AnnotationGroup":
        return AnnotationGroup(self.name, self.classes, exclusive)

    def add_class(self, class_name: str) -> "AnnotationGroup":
        if class_name in self.classes:
            raise ValueError(f"Class {class_name} already exists in the group.")
        return AnnotationGroup(self.name, self.classes + [class_name], self.exclusive)

    def remove_class(self, class_name: str) -> "AnnotationGroup":
        if class_name not in self.classes:
            raise ValueError(f"Class {class_name} does not exist in the group.")
        return AnnotationGroup(
            self.name, [c for c in self.classes if c != class_name], self.exclusive
        )

    def rename_class(self, old_name: str, new_name: str) -> "AnnotationGroup":
        if old_name not in self.classes:
            raise ValueError(f"Class {old_name} does not exist in the group.")
        if new_name in self.classes:
            raise ValueError(f"Class {new_name} already exists in the group.")
        return AnnotationGroup(
            self.name,
            [new_name if c == old_name else c for c in self.classes],
            self.exclusive,
        )

    def rearrange_classes(self, new_order: list[str]) -> "AnnotationGroup":
        if set(new_order) != set(self.classes):
            raise ValueError("Re-ordering classes must match the group classes.")
        return AnnotationGroup(self.name, new_order, self.exclusive)


@dataclass(frozen=True, eq=True)
class AnnotationSchema:
    groups: list[AnnotationGroup] = field(default_factory=list)

    def get_group(self, name: str) -> AnnotationGroup:
        return next(g for g in self.groups if g.name == name)

    def group_names(self) -> list[str]:
        return [g.name for g in self.groups]

    def add_group(self, group: AnnotationGroup) -> "AnnotationSchema":
        if group.name in self.group_names():
            raise ValueError(f"Group {group.name} already exists in the schema.")
        return AnnotationSchema(self.groups + [group])

    def remove_group(self, group: Union[str, AnnotationGroup]) -> "AnnotationSchema":
        name = group if isinstance(group, str) else group.name
        if name not in self.group_names():
            raise ValueError(f"Group {name} does not exist in the schema.")
        return AnnotationSchema([g for g in self.groups if g.name != name])

    def rename_group(self, old_name: str, new_name: str) -> "AnnotationSchema":
        if old_name not in self.group_names():
            raise ValueError(f"Group {old_name} does not exist in the schema.")
        if new_name in self.group_names():
            raise ValueError(f"Group {new_name} already exists in the schema.")
        return AnnotationSchema(
            [g.rename(new_name) if g.name == old_name else g for g in self.groups]
        )

    def update_group(self, new_group: AnnotationGroup):
        if new_group.name not in self.group_names():
            raise ValueError(f"Group {new_group.name} does not exist in the schema.")
        return AnnotationSchema(
            [new_group if g.name == new_group.name else g for g in self.groups]
        )

    def rearrange_names(self, names: list[str]) -> "AnnotationSchema":
        if set(names) != set(self.group_names()):
            raise ValueError("Re-ordering names must match the schema.")
        return AnnotationSchema([self.get_group(name) for name in names])


@dataclass(frozen=True, eq=True)
class AnnotatedGroup:
    group: AnnotationGroup
    classes: list[str] = field(default_factory=list)

    def __post_init__(self):
        assert isinstance(self.group, AnnotationGroup)
        assert all(isinstance(c, str) for c in self.classes)
        assert set(self.classes).issubset(set(self.group.classes))

    def is_valid(self) -> bool:
        """Validates if the classes in this group are valid according to the AnnotationGroup definition."""
        if not set(self.classes).issubset(set(self.group.classes)):
            return False
        if self.group.exclusive and len(self.classes) > 1:
            return False
        return True

    def update(
        self,
        new_group: AnnotationGroup,
        renaming_map: dict[str, str],
    ) -> "AnnotatedGroup":
        """Updates the AnnotatedGroup according to the new AnnotationGroup and class renaming."""
        valid_classes = set(new_group.classes)
        new_classes = [
            renaming_map.get(c, c)
            for c in self.classes
            if renaming_map.get(c, c) in valid_classes
        ]

        if len(new_classes) > 1 and new_group.exclusive:
            new_classes = []  # Reset classes if exclusive group has more than one class

        new_group = AnnotatedGroup(new_group, new_classes)
        assert new_group.is_valid()
        return new_group


@dataclass(frozen=True, eq=True)
class Annotation:
    file: Path
    schema: AnnotationSchema
    groups: list[AnnotatedGroup] = field(default_factory=list)

    def __post_init__(self):
        assert isinstance(self.file, Path)
        assert isinstance(self.schema, AnnotationSchema)
        assert all(isinstance(g, AnnotatedGroup) for g in self.groups)

    def validate_annotations(self) -> bool:
        defined_groups = self.schema.group_names()
        annotated_groups = [g.group.name for g in self.groups]

        if annotated_groups != defined_groups:
            # Check if all groups are present in the annotation
            return False

        return all(annotated_group.is_valid() for annotated_group in self.groups)

    def update(
        self,
        new_schema: AnnotationSchema,
        group_renaming_map: dict[str, str],
        class_renaming_map: dict[str, dict[str, str]],
    ) -> "Annotation":
        assert isinstance(new_schema, AnnotationSchema)
        assert all(isinstance(v, str) for v in group_renaming_map.values())
        assert all(isinstance(v, dict) for v in class_renaming_map.values())

        """Updates the annotation according to the new groups and renaming maps."""
        new_annotated_groups = []
        map_new_to_old = {v: k for k, v in group_renaming_map.items()}
        if len(map_new_to_old) != len(group_renaming_map):
            raise ValueError("Group renaming map is not bijective.")
        if len(map_new_to_old) > len(new_schema.groups):
            raise ValueError("Group renaming map is too large.")

        for new_group in new_schema.groups:
            if new_group.name not in map_new_to_old:
                # Create a new annotated group for new groups
                new_annotated_groups.append(AnnotatedGroup(new_group, []))
                continue

            # Has to exist, otherwise the renaming map is wrong
            old_group_name = map_new_to_old[new_group.name]
            old_annotated_group = next(
                (g for g in self.groups if g.group.name == old_group_name),
                None,
            )

            if old_annotated_group is None:
                raise ValueError(
                    f"Old annotated group {old_group_name} not found in current annotations."
                )

            if old_group_name not in class_renaming_map:
                raise ValueError(
                    f"No class renaming map provided for old group {old_group_name}."
                )

            # Update the classes according to the renaming map
            new_annotated_group = old_annotated_group.update(
                new_group, class_renaming_map[old_group_name]
            )

            new_annotated_groups.append(new_annotated_group)

        new_annotation = Annotation(self.file, new_schema, new_annotated_groups)
        if not new_annotation.validate_annotations():
            raise ValueError("Updated annotation failed validation.")
        return new_annotation

    def is_empty(self):
        return all(len(g.classes) == 0 for g in self.groups)


@dataclass(frozen=True, eq=True)
class ProjectSettings:
    name: str
    file: Path
    schema: AnnotationSchema = field(default_factory=AnnotationSchema)
    file_paths: list[Path] = field(default_factory=list, repr=False)
    output_file: Optional[Path] = None

    def __post_init__(self):
        assert isinstance(self.file, Path)
        assert isinstance(self.schema, AnnotationSchema)
        assert len(self.file_paths) > 0
        assert all(isinstance(p, Path) for p in self.file_paths)
        if self.output_file is not None:
            assert isinstance(self.output_file, Path)


@dataclass(frozen=True, eq=True)
class GroupFilter:
    group: AnnotationGroup
    valid_classes: list[str] = field(default_factory=list)

    def __post_init__(self):
        assert isinstance(self.group, AnnotationGroup)
        assert all(isinstance(s, str) for s in self.valid_classes)
        assert set(self.valid_classes).issubset(set(self.group.classes))

    @property
    def name(self):
        return self.group.name

    @property
    def is_active(self) -> bool:
        return 0 < len(self.valid_classes) < len(self.group.classes)

    def matches(self, group: AnnotatedGroup) -> bool:
        assert group.group.name == self.group.name
        assert set(group.classes).issubset(set(self.group.classes))

        if self.is_active:
            return set(group.classes).issubset(set(self.valid_classes))
        return True

    def reset(self) -> "GroupFilter":
        return GroupFilter(self.group, [])


@dataclass(frozen=True, eq=True)
class Filter:
    schema: AnnotationSchema
    group_filters: list[GroupFilter]

    def __post_init__(self):
        assert isinstance(self.schema, AnnotationSchema)
        assert all(isinstance(g, GroupFilter) for g in self.group_filters)

    @staticmethod
    def from_schema(schema: AnnotationSchema) -> "Filter":
        return Filter(schema, [GroupFilter(g) for g in schema.groups])

    @property
    def is_active(self) -> bool:
        return (
            any(g.is_active for g in self.group_filters) and len(self.group_filters) > 0
        )

    def matches(self, annotation: Annotation) -> bool:
        if self.is_active:
            return all(
                g.matches(a) for g, a in zip(self.group_filters, annotation.groups)
            )
        return True

    def reset(self) -> "Filter":
        return self.from_schema(self.schema)


@dataclass
class Project:
    settings: ProjectSettings = field(default_factory=ProjectSettings)
    _annotations: list[Annotation] = field(default_factory=list, init=False)
    _filter: Filter = field(init=False)
    _valid_indices: list[int] = field(init=False)

    def _save_add_annotation(self, annotation: Annotation):
        if annotation.validate_annotations():
            self._annotations.append(annotation)
        else:
            raise ValueError("Invalid annotation according to the project settings.")

    def __post_init__(self):
        assert isinstance(self.settings, ProjectSettings)
        assert all(isinstance(a, Annotation) for a in self._annotations)

        self._annotations = []
        for file in self.settings.file_paths:
            annotated_groups = []
            for group in self.settings.schema.groups:
                annotated_groups.append(AnnotatedGroup(group))
            annotation = Annotation(file, self.settings.schema, annotated_groups)
            self._save_add_annotation(annotation)

        self._filter = Filter.from_schema(self.settings.schema)
        self._valid_indices = list(range(len(self._annotations)))

    def to_dataframe(self) -> pd.DataFrame:
        data = []

        # Iterate over each annotation in the project
        for annotation in self._annotations:
            row = {"ImagePath": annotation.file}

            # Flatten the annotations into columns "{group_name}[SEP]{class_name}"
            for annotated_group in annotation.groups:
                group_name = annotated_group.group.name
                for class_name in annotated_group.group.classes:
                    seperator = common.get_config().group_class_separator
                    column_name = f"{group_name}{seperator}{class_name}"
                    # Set binary values for the presence of a class in this specific annotation
                    row[column_name] = 1 if class_name in annotated_group.classes else 0

            data.append(row)

        # Create DataFrame from the list of data
        df = pd.DataFrame(data)

        # Fill missing values with 0 (for classes not annotated in some images)
        df.fillna(0, inplace=True)

        return df

    def to_disk(self):
        file_path = self.settings.file
        with open(file_path, "wb") as file:
            pickle.dump(self, file)

        if self.settings.output_file is not None:
            df = self.to_dataframe()
            df.to_csv(self.settings.output_file, index=False)

    @staticmethod
    def from_disk(path: Path):
        """Loads a project from a specified path."""
        with open(path, "rb") as file:
            project = pickle.load(file)
        return project

    def apply_renaming_mapping(
        self,
        group_renaming: dict[str, str],
        class_renaming: dict[str, dict[str, str]],
        old_logic: bool = True,
    ):
        if old_logic:
            group_renaming, class_renaming = common.invert_translation_dicts(
                group_renaming, class_renaming
            )
        else:
            raise NotImplementedError("New logic not implemented yet.")

        self._annotations = [
            annotation.update(self.settings.schema, group_renaming, class_renaming)
            for annotation in self._annotations
        ]

    def set_filter(self, filter: Filter):
        if filter != self._filter:
            self._filter = filter
            self._valid_indices = []
            for idx, annotation in enumerate(self._annotations):
                assert isinstance(annotation, Annotation)
                assert annotation.validate_annotations()
                if filter.matches(annotation):
                    self._valid_indices.append(idx)  # Save the valid index

    def __len__(self) -> int:
        return len(self._valid_indices)

    def __getitem__(self, idx: int) -> Annotation:
        mapped_idx = self._valid_indices[idx]

        assert 0 <= idx <= len(self._valid_indices)
        assert 0 <= mapped_idx <= len(self._annotations)

        annotation: Annotation = self._annotations[mapped_idx]

        assert isinstance(annotation, Annotation) and annotation.validate_annotations()

        return annotation

    def __setitem__(self, idx: int, value: Annotation) -> None:
        mapped_idx = self._valid_indices[idx]

        assert isinstance(value, Annotation) and value.validate_annotations()
        assert 0 <= idx <= len(self._valid_indices)
        assert 0 <= mapped_idx <= len(self._annotations)

        self._annotations[mapped_idx] = value

    @property
    def name(self):
        return self.settings.name

    @property
    def annotations(self) -> list[Annotation]:
        return [self[i] for i in range(len(self))]  # Return all valid annotations

    @property
    def filter(self) -> Filter:
        return self._filter
