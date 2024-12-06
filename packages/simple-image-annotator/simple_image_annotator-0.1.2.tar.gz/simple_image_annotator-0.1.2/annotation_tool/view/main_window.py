from dataclasses import replace
from pathlib import Path
from typing import Optional

import PyQt6.QtCore as qtc
from PyQt6.QtCore import Qt
import PyQt6.QtGui as qtg
from PyQt6.QtGui import QPalette, QStandardItem
import PyQt6.QtWidgets as qtw

from annotation_tool import common, model
from annotation_tool.view.helper_widgets import (
    OpenGLImageViewer,
    RangeIntValidator,
    build_separator,
    simulate_key_press,
)


class AnnotationGroupWidget(qtw.QGroupBox):
    selection_changed = qtc.pyqtSignal(list)

    def __init__(self, name: str, exclusive: bool, classes: list[str], *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.name = name
        self.exclusive = exclusive
        self.classes = classes
        self.init_ui()

    def init_ui(self):
        layout = qtw.QVBoxLayout(self)
        self.buttons = {}
        for class_name in self.classes:
            btn = qtw.QPushButton(class_name)
            btn.setStyleSheet("QPushButton:checked { background-color: lightgreen; }")
            btn.setCheckable(True)
            btn.clicked.connect(self.change_selection)
            layout.addWidget(btn)
            self.buttons[class_name] = btn

    def set_annotation(self, selected_classes: list[str]):
        for class_name, btn in self.buttons.items():
            btn.setChecked(class_name in selected_classes)

    @property
    def selected_classes(self) -> list[str]:
        return [cls for cls, btn in self.buttons.items() if btn.isChecked()]

    def change_selection(self):
        clicked_button = self.sender()
        if clicked_button.isChecked():
            if self.exclusive:
                for btn in self.buttons.values():
                    if btn != clicked_button:
                        btn.setChecked(False)
            self.selection_changed.emit(self.selected_classes)
        else:
            clicked_button.setChecked(False)
            self.selection_changed.emit(self.selected_classes)

    def __del__(self):
        print("AnnotationGroup deleted")


class AnnotationPanel(qtw.QWidget):
    annotation_changed = qtc.pyqtSignal(model.Annotation)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(qtw.QVBoxLayout())
        self.schema = None
        self._orignal_annotation = None
        self.group_widgets = {}

    def clear(self):
        for i in reversed(range(self.layout().count())):
            layout_item = self.layout().itemAt(i)
            group_widget = layout_item.widget()
            if group_widget:
                if isinstance(group_widget, AnnotationGroupWidget):
                    group_widget.selection_changed.disconnect()
                    assert group_widget in self.group_widgets
                    del self.group_widgets[group_widget]
                group_widget.deleteLater()
            self.layout().removeItem(layout_item)

        assert self.layout().count() == 0
        assert len(self.group_widgets) == 0

    def set_schema(self, schema: Optional[model.AnnotationSchema]):
        self.schema = schema
        self.clear()
        for group in schema.groups:
            group_widget = AnnotationGroupWidget(
                group.name, group.exclusive, group.classes
            )
            assert group_widget not in self.group_widgets
            self.group_widgets[group_widget] = group
            group_widget.selection_changed.connect(self.handle_selection_change)
            self.layout().addWidget(group_widget)

    @property
    def current_annotation(self) -> model.Annotation:
        assert self._orignal_annotation is not None

        annotations = []
        for idx, (group_widget, group) in enumerate(self.group_widgets.items()):
            assert isinstance(group_widget, AnnotationGroupWidget)
            assert isinstance(group, model.AnnotationGroup)
            assert (
                group == self.schema.groups[idx]
            ), f"Order of groups changed {group} != {self.schema.groups[idx]}"
            assert (
                group_widget.name == group.name
            ), f"{group_widget.name} != {group.name}"
            annotations.append(
                model.AnnotatedGroup(group, group_widget.selected_classes)
            )

        return replace(self._orignal_annotation, groups=annotations)

    def handle_selection_change(self, *args, **kwargs):
        self.annotation_changed.emit(self.current_annotation)

    def set_annotation(self, annotation: model.Annotation):
        assert isinstance(annotation, model.Annotation)
        assert annotation.schema == self.schema
        groups = annotation.groups

        assert len(groups) == self.layout().count() == len(self.group_widgets)

        for idx, group_widget in enumerate(self.group_widgets):
            assert group_widget == self.layout().itemAt(idx).widget()
            assert isinstance(group_widget, AnnotationGroupWidget)

            group: model.AnnotatedGroup = groups[idx]
            assert group_widget.name == group.group.name

            group_widget.set_annotation(groups[idx].classes)

        self._orignal_annotation = annotation
        assert self.current_annotation == annotation


class CheckableComboBox(qtw.QComboBox):
    # Subclass Delegate to increase item height
    class Delegate(qtw.QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        palette = qtw.QApplication.palette()
        palette.setBrush(QPalette.ColorRole.Base, palette.button())
        self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):
        if object == self.lineEdit():
            if event.type() == qtc.QEvent.Type.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == qtc.QEvent.Type.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == qtc.Qt.CheckState.Checked:
                    item.setCheckState(qtc.Qt.CheckState.Unchecked)
                else:
                    item.setCheckState(qtc.Qt.CheckState.Checked)
                return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing

        self.updateText()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        self.lineEdit().setText(self.name)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(
            qtc.Qt.ItemFlag.ItemIsEnabled | qtc.Qt.ItemFlag.ItemIsUserCheckable
        )
        item.setData(qtc.Qt.CheckState.Unchecked, qtc.Qt.ItemDataRole.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == qtc.Qt.CheckState.Checked:
                res.append(self.model().item(i).data())
        return res

    def getItemByIndex(self, index):
        return self.model().item(index)

    def setChecked(self, idx):
        assert 0 <= idx < self.model().rowCount()
        self.getItemByIndex(idx).setCheckState(qtc.Qt.CheckState.Checked)

    def findText(self, text):
        for i in range(self.model().rowCount()):
            if self.model().item(i).text() == text:
                return i
        return -1

    def getItems(self) -> list[QStandardItem]:
        items = []
        for i in range(self.model().rowCount()):
            items.append(self.model().item(i))
        return items


class FilterPanel(qtw.QWidget):
    filter_changed = qtc.pyqtSignal(model.Filter)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = None
        self._original_filter = None
        self.dropdowns = {}
        self.init_ui()

    def init_ui(self):
        self.setLayout(qtw.QGridLayout())

        combobox_widget = qtw.QWidget(self)
        self.combobox_layout = qtw.QVBoxLayout(combobox_widget)
        self.layout().addWidget(combobox_widget, 0, 0, 1, 2)

        apply_button = qtw.QPushButton("Apply")
        apply_button.clicked.connect(
            lambda: self.filter_changed.emit(self.current_filters)
        )
        reset_button = qtw.QPushButton("Reset")
        reset_button.clicked.connect(self.reset)

        # Position buttons at the bottom of the layout
        self.layout().addWidget(apply_button, self.layout().rowCount(), 0)
        self.layout().addWidget(reset_button, self.layout().rowCount() - 1, 1)

    def clear(self):
        for i in reversed(range(self.combobox_layout.count())):
            layout_item = self.combobox_layout.itemAt(i)
            widget = layout_item.widget()
            if widget:
                if isinstance(widget, CheckableComboBox):
                    assert widget in self.dropdowns
                    del self.dropdowns[widget]
                widget.deleteLater()
            self.combobox_layout.removeItem(layout_item)

        assert self.combobox_layout.count() == 0
        assert len(self.dropdowns) == 0

    def set_schema(self, schema: model.AnnotationSchema):
        self.clear()
        self.schema = schema
        for group in schema.groups:
            dropdown = CheckableComboBox(group.name)
            dropdown.addItems(group.classes)
            self.dropdowns[dropdown] = group
            self.combobox_layout.addWidget(dropdown)

    @property
    def current_filters(self) -> model.Filter:
        assert self._original_filter is not None

        group_filters = []
        for dropdown, group in self.dropdowns.items():
            valid_classes = dropdown.currentData()
            assert all(cls in group.classes for cls in valid_classes)
            group_filters.append(model.GroupFilter(group, valid_classes))

        return replace(self._original_filter, group_filters=group_filters)

    def set_filter(self, filter: model.Filter):
        assert isinstance(filter, model.Filter)
        assert filter.schema == self.schema

        groups = filter.group_filters
        assert len(groups) == self.combobox_layout.count() == len(self.dropdowns)

        for idx, dropdown in enumerate(self.dropdowns):
            assert dropdown == self.combobox_layout.itemAt(idx).widget()
            assert isinstance(dropdown, CheckableComboBox)

            valid_classes = filter.group_filters[idx].valid_classes
            group = groups[idx].group

            assert dropdown.name == group.name
            assert len(dropdown.getItems()) == len(group.classes)

            for item in dropdown.getItems():
                item.setCheckState(
                    qtc.Qt.CheckState.Checked
                    if item.data() in valid_classes
                    else qtc.Qt.CheckState.Unchecked
                )

        self._original_filter = filter
        assert self.current_filters == filter

    def reset(self):
        assert self.schema is not None
        self.set_filter(model.Filter.from_schema(self.schema))
        self.filter_changed.emit(self.current_filters)


class GUI(qtw.QMainWindow):
    jump_to = qtc.pyqtSignal((common.JumpType,), (int,))
    change_annotation = qtc.pyqtSignal(model.Annotation)
    change_filters = qtc.pyqtSignal(model.Filter)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(1200, 800)
        self.setWindowTitle("Annotation Tool")
        self.write_to_status_bar("Ready")
        self.annotation_panel = None
        self.filter_panel = None
        self._last_image_path = None

        # Create menu bar and add a direct action for settings
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        self.new_project_action = qtg.QAction("&New Project", self)
        self.open_project_action = qtg.QAction("&Open Project", self)
        self.update_project_action = qtg.QAction("&Update Project", self)
        self.save_project_action = qtg.QAction("&Save Project", self)
        self.settings_action = qtg.QAction("&Settings", self)
        self.close_project_action = qtg.QAction("&Close Project", self)
        self.exit_action = qtg.QAction("&Exit", self)

        file_menu.addAction(self.new_project_action)
        file_menu.addAction(self.open_project_action)
        file_menu.addAction(self.update_project_action)
        file_menu.addAction(self.save_project_action)
        file_menu.addAction(self.settings_action)
        file_menu.addAction(self.close_project_action)
        file_menu.addAction(self.exit_action)

        self.init_ui()
        self.init_shortcuts()

    def init_ui(self):
        # central widget
        central_widget = qtw.QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = qtw.QVBoxLayout(central_widget)

        # widgets
        top_panel = self._init_top_panel()
        bottom_panel = self._init_bottom_panel()

        main_layout.addWidget(top_panel, 95)
        main_layout.addWidget(build_separator("horizontal", self))
        main_layout.addWidget(bottom_panel, 5)

    def _init_top_panel(self):
        top_panel = qtw.QWidget(self)
        top_layout = qtw.QHBoxLayout(top_panel)

        # Image display
        keep_aspect_ratio = common.get_config().keep_aspectratio
        self.image_display = OpenGLImageViewer()
        self.image_display.set_keep_aspect_ratio(keep_aspect_ratio)
        top_layout.addWidget(self.image_display, 80)
        top_layout.addWidget(build_separator("vertical", self))

        # Right panel (filter and annotation)
        right_panel = qtw.QWidget(self)
        self.right_layout = qtw.QVBoxLayout(right_panel)

        # Filter panel
        self.filter_panel = FilterPanel(self)
        self.filter_panel.filter_changed.connect(self.change_filters)
        self.right_layout.addWidget(self.filter_panel)

        # Separator
        self.right_layout.addWidget(build_separator("horizontal", self))
        self.right_layout.addStretch(1)

        # Annotation panel
        self.annotation_panel = AnnotationPanel(self)
        self.annotation_panel.annotation_changed.connect(self.change_annotation)
        self.right_layout.addWidget(self.annotation_panel)

        top_layout.addWidget(right_panel, 20)

        return top_panel

    def _init_bottom_panel(self):
        bottom_panel = qtw.QWidget(self)
        bottom_layout = qtw.QHBoxLayout(bottom_panel)

        # Label showing the current position
        self.position_label = qtw.QLabel(self)
        bottom_layout.addWidget(self.position_label)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(build_separator("vertical", self))
        bottom_layout.addStretch(1)

        # Navigation buttons
        self.btnGoToStart = qtw.QPushButton("Start")
        self.btnGoToStart.clicked.connect(
            lambda: self.jump_to.emit(common.JumpType.START)
        )
        bottom_layout.addWidget(self.btnGoToStart)

        self.btnGoToPrevious = qtw.QPushButton("Previous")
        self.btnGoToPrevious.clicked.connect(
            lambda: self.jump_to.emit(common.JumpType.PREV)
        )
        bottom_layout.addWidget(self.btnGoToPrevious)

        self.btnGoToNext = qtw.QPushButton("Next")
        self.btnGoToNext.clicked.connect(
            lambda: self.jump_to.emit(common.JumpType.NEXT)
        )

        bottom_layout.addWidget(self.btnGoToNext)

        self.btnGoToEnd = qtw.QPushButton("End")
        self.btnGoToEnd.clicked.connect(lambda: self.jump_to.emit(common.JumpType.END))
        bottom_layout.addWidget(self.btnGoToEnd)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(build_separator("vertical", self))
        bottom_layout.addStretch(1)

        self.btnGoToFirstNonAnnotated = qtw.QPushButton("First Non-Annotated")
        self.btnGoToFirstNonAnnotated.clicked.connect(
            lambda: self.jump_to.emit(common.JumpType.FIRST_EMPTY)
        )
        bottom_layout.addWidget(self.btnGoToFirstNonAnnotated)

        bottom_layout.addStretch(1)
        bottom_layout.addWidget(build_separator("vertical", self))
        bottom_layout.addStretch(1)

        # Search bar
        self.index_field = qtw.QLineEdit(self)
        self.index_field.setValidator(RangeIntValidator(0, 0))
        self.index_field.setPlaceholderText("Index")
        self.index_field.returnPressed.connect(self.apply_index_search)
        bottom_layout.addWidget(self.index_field)

        self.search_button = qtw.QPushButton("Search")
        self.search_button.clicked.connect(self.apply_index_search)
        bottom_layout.addWidget(self.search_button)

        return bottom_panel

    def init_shortcuts(self):
        # Shortcuts
        self.save_shortcut = qtg.QShortcut(qtg.QKeySequence.StandardKey.Save, self)
        self.left_shortcut = qtg.QShortcut(qtg.QKeySequence("Left"), self)
        self.right_shortcut = qtg.QShortcut(qtg.QKeySequence("Right"), self)
        self.reload_shortcut = qtg.QShortcut(qtg.QKeySequence("Ctrl+R"), self)
        self.focus_shortcut = qtg.QShortcut(
            qtg.QKeySequence("Ctrl+F"),
            self,
            activated=self.focus_on_annotation_buttons,
        )

        self._setup_initial_focus()

    def apply_index_search(self):
        parsed_text = self.index_field.text()
        if parsed_text:
            idx = int(parsed_text) - 1  # conv to zero-indexing
            self.index_field.clear()
            self.jump_to[int].emit(idx)

    def set_annotation(self, annotation: model.Annotation):
        assert isinstance(annotation, model.Annotation)
        self.annotation_panel.set_annotation(annotation)

    def _setup_initial_focus(self):
        try:
            self.focus_on_annotation_buttons()
            simulate_key_press(self, Qt.Key.Key_Tab)
            simulate_key_press(self, Qt.Key.Key_Tab, Qt.KeyboardModifier.ShiftModifier)
        except Exception:  # noqa
            pass

    def focus_on_annotation_buttons(self):
        if self.annotation_panel:
            self.annotation_panel.setFocus()

            return
            if self.annotation_panel.annotation_group_map:
                btn = next(iter(self.annotation_panel.annotation_group_map.values()))

            btn = next(iter(self.annotation_buttons.values()))
            btn.setFocus()

    def set_filter(self, filter: model.Filter):
        assert isinstance(filter, model.Filter)
        self.filter_panel.set_filter(filter)

    def set_position(self, pos, total):
        self.btnGoToStart.setDisabled(pos == 0)
        self.btnGoToPrevious.setDisabled(pos == 0)
        self.btnGoToEnd.setDisabled(pos == total - 1)
        self.btnGoToNext.setDisabled(pos == total - 1)
        self.position_label.setText(f"{pos + 1}/{total}")
        self.index_field.validator().setRange(1, total)

    def set_image(self, image_path: Path):
        self._last_image_path = image_path
        self.image_display.set_image(image_path)

    def write_to_status_bar(self, message):
        self.statusBar().showMessage(message, 5000)

    def clear(self):
        print("Clearing GUI")
        self.position_label.clear()
        self.image_display.clear()
        self.annotation_panel.clear()
        # self.set_filters({})

    def set_schema(self, schema: model.AnnotationSchema):
        assert isinstance(schema, model.AnnotationSchema)
        self.annotation_panel.set_schema(schema)
        self.filter_panel.set_schema(schema)

    def settings_changed(self):
        keep_aspect_ratio = common.get_config().keep_aspectratio
        self.image_display.set_keep_aspect_ratio(keep_aspect_ratio)
