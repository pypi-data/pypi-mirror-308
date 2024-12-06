from copy import deepcopy
from pathlib import Path
from typing import Optional, Union

import PyQt6.QtCore as qtc
from PyQt6.QtCore import Qt
import PyQt6.QtGui as qtg
import PyQt6.QtWidgets as qtw

from annotation_tool import common, model
from annotation_tool.view import (
    GUI,
    OpenProjectDialog,
    SettingsDialog,
    UpdateProjectDialog,
)


class MainApplication(qtw.QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = None
        self.project: model.Project = None

        # timer for automatic saving
        self.save_timer = qtc.QTimer()
        self.save_timer.timeout.connect(self.save_project)
        self.save_timer.start(common.SAVE_INTERVAL_IN_SECONDS * 1000)

        # setup design
        self.init_theme()
        self.gui = GUI()

        # Connect gui signals
        self.gui.jump_to[common.JumpType].connect(self.handle_jump)
        self.gui.jump_to[int].connect(self.handle_jump)
        self.gui.change_annotation.connect(self.update_annotation)
        self.gui.change_filters.connect(self.handle_filter_update)

        # Connect gui shortcuts
        self.gui.save_shortcut.activated.connect(self.save_project)
        self.gui.left_shortcut.activated.connect(
            lambda: self.handle_jump(common.JumpType.PREV)
        )
        self.gui.right_shortcut.activated.connect(
            lambda: self.handle_jump(common.JumpType.NEXT)
        )
        self.gui.reload_shortcut.activated.connect(self.handle_filter_update)

        # Connect menu actions
        self.gui.new_project_action.triggered.connect(self.create_project)
        self.gui.open_project_action.triggered.connect(self.open_project)
        self.gui.update_project_action.triggered.connect(self.update_project)
        self.gui.save_project_action.triggered.connect(self.save_project)
        self.gui.settings_action.triggered.connect(self.open_settings)
        self.gui.close_project_action.triggered.connect(self._init_project)
        self.gui.exit_action.triggered.connect(self.quit)

        self.gui.show()

        # open recent project
        project = None
        if common.get_config().previous_project:
            try:
                project = model.Project.from_disk(common.get_config().previous_project)
            except Exception as e:
                print(f"Failed to load project: {e}")

        self._init_project(project)

    def _init_project(
        self, project: Optional[model.Project], target_position: Optional[int] = None
    ):
        self.project = project
        self.gui.clear()

        new_file = project.settings.file if self.project else None
        conf = common.get_config().update_project(new_file)
        common.write_config(conf)

        if self.project:
            self.project.to_disk()
            self.gui.set_schema(self.project.settings.schema)
            self.gui.set_filter(self.project.filter)
            if target_position is None:
                self.handle_jump(common.JumpType.FIRST_EMPTY, force=True)
            else:
                self.handle_jump(target_position, force=True)

    def create_project(self):
        dlg = UpdateProjectDialog()
        if dlg.exec() == qtw.QDialog.DialogCode.Accepted:
            self._init_project(model.Project(dlg.settings))

    def update_project(self):
        current_project = self.project

        if current_project is None:
            return

        assert isinstance(current_project, model.Project)

        dlg = UpdateProjectDialog(self.project)
        if dlg.exec() == qtw.QDialog.DialogCode.Accepted:
            updated_settings = dlg.settings

            if updated_settings == current_project.settings:
                return  # nothing changed

            updated_project = deepcopy(current_project)
            updated_project.settings = updated_settings

            if updated_settings.schema != current_project.settings.schema:
                # Schema changed -> Rename groups and classes and reset filter
                translate_groups = dlg.record_group_names
                translate_classes = dlg.record_class_names
                updated_project.apply_renaming_mapping(
                    translate_groups, translate_classes
                )
                updated_project.set_filter(
                    model.Filter.from_schema(updated_project.settings.schema)
                )

                if current_project.filter.is_active:
                    # Moving from filter to no filter -> Jump to first empty annotation
                    self._init_project(updated_project)
                else:
                    # Moving from no filter to filter -> Keep current position
                    self._init_project(updated_project, self.position)
            else:
                # Schema did not change -> Keep current position
                self._init_project(updated_project, self.position)

    def open_project(self):
        dlg = OpenProjectDialog()
        if dlg.exec() == qtw.QDialog.DialogCode.Accepted:
            self._init_project(dlg.project)

    def open_settings(self):
        config = common.get_config()
        dlg = SettingsDialog(config)
        if dlg.exec() == qtw.QDialog.DialogCode.Accepted:
            new_config = dlg.config
            if new_config != config:
                common.write_config(new_config)
                self.gui.settings_changed()

    def save_project(self):
        if self.project:
            self.project.to_disk()
            project_path = self.project.settings.file.as_posix()
            self.gui.write_to_status_bar(f"Saved project to {project_path}.")

    @property
    def num_annotations(self) -> int:
        return len(self.project) if self.project else 0

    @property
    def current_annotation(self) -> model.Annotation:
        return self.project[self.position]

    @property
    def current_image(self) -> Path:
        return self.project[self.position].file

    def _jump_abs(self, new_pos, force=False):
        if force:
            self.position = None

        new_pos = max(0, min(len(self.project) - 1, new_pos))  # clamp to valid range
        if new_pos != self.position:
            self.position = new_pos
            self.gui.set_image(self.current_image)
            self.gui.set_position(new_pos, len(self.project))
            self.gui.set_annotation(self.current_annotation)

    def _find_first_empty_annotation(self):
        # Really slow, but should be fine for now
        for idx, anno in enumerate(self.project.annotations):
            if anno.is_empty():
                return idx
        return 0

    def handle_jump(self, target: Union[common.JumpType, int], force: bool = False):
        if self.project:
            if target == common.JumpType.START:
                self._jump_abs(0, force)
            elif target == common.JumpType.PREV:
                self._jump_abs(self.position - 1, force)
            elif target == common.JumpType.NEXT:
                self._jump_abs(self.position + 1, force)
            elif target == common.JumpType.END:
                self._jump_abs(len(self.project) - 1, force)
            elif target == common.JumpType.FIRST_EMPTY:
                self._jump_abs(self._find_first_empty_annotation(), force)
            elif isinstance(target, int):
                self._jump_abs(target, force)
            else:
                raise RuntimeError(f"Unknown jump target: {target}")

    def init_theme(self):
        font = qtg.QFont()
        font.setPointSize(common.get_config().font_size)
        self.setFont(font)

        self.setStyle("Fusion")

        # # Now use a palette to switch to dark colors:
        dark_palette = qtg.QPalette(self.style().standardPalette())
        dark_palette.setColor(qtg.QPalette.ColorRole.Window, qtg.QColor(53, 53, 53))
        dark_palette.setColor(qtg.QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(qtg.QPalette.ColorRole.Base, qtg.QColor(35, 35, 35))
        dark_palette.setColor(
            qtg.QPalette.ColorRole.AlternateBase, qtg.QColor(53, 53, 53)
        )
        dark_palette.setColor(
            qtg.QPalette.ColorRole.ToolTipBase, qtg.QColor(25, 25, 25)
        )
        dark_palette.setColor(qtg.QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(qtg.QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(qtg.QPalette.ColorRole.Button, qtg.QColor(53, 53, 53))
        dark_palette.setColor(qtg.QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(qtg.QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        dark_palette.setColor(qtg.QPalette.ColorRole.Link, qtg.QColor(42, 130, 218))
        dark_palette.setColor(
            qtg.QPalette.ColorRole.Highlight, qtg.QColor(42, 130, 218)
        )
        dark_palette.setColor(
            qtg.QPalette.ColorRole.HighlightedText, qtg.QColor(35, 35, 35)
        )
        dark_palette.setColor(
            qtg.QPalette.ColorGroup.Active,
            qtg.QPalette.ColorRole.Button,
            qtg.QColor(53, 53, 53),
        )
        dark_palette.setColor(
            qtg.QPalette.ColorGroup.Disabled,
            qtg.QPalette.ColorRole.ButtonText,
            Qt.GlobalColor.darkGray,
        )
        dark_palette.setColor(
            qtg.QPalette.ColorGroup.Disabled,
            qtg.QPalette.ColorRole.WindowText,
            Qt.GlobalColor.darkGray,
        )
        dark_palette.setColor(
            qtg.QPalette.ColorGroup.Disabled,
            qtg.QPalette.ColorRole.Text,
            Qt.GlobalColor.darkGray,
        )
        dark_palette.setColor(
            qtg.QPalette.ColorGroup.Disabled,
            qtg.QPalette.ColorRole.Light,
            qtg.QColor(53, 53, 53),
        )
        self.setPalette(dark_palette)

    def handle_filter_update(self, filter: model.Filter):
        assert self.project is not None
        assert isinstance(filter, model.Filter)

        if filter != self.project.filter:
            self.project.set_filter(filter)
            self.handle_jump(common.JumpType.FIRST_EMPTY, force=True)

    def update_annotation(self, annotation: model.Annotation):
        assert self.project is not None
        assert isinstance(annotation, model.Annotation)
        assert annotation.schema == self.project.settings.schema
        assert self.project[self.position].file == annotation.file
        if self.project:
            print("Update annotation:", annotation.groups)
            self.project[self.position] = annotation
