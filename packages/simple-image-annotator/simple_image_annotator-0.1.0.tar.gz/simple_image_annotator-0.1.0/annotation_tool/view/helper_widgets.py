from pathlib import Path
from typing import Union

import OpenGL.GL as gl
from PyQt6.QtCore import Qt
import PyQt6.QtGui as qtg
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
import PyQt6.QtWidgets as qtw
import cv2
import numpy as np


def simulate_key_press(widget, key, modifier=Qt.KeyboardModifier.NoModifier):
    event = qtg.QKeyEvent(qtg.QKeyEvent.Type.KeyPress, key, modifier)
    qtw.QApplication.postEvent(widget, event)


def open_image_as_rgb(image_path: Union[str, Path], return_flipped=False):
    image_path = image_path.as_posix() if isinstance(image_path, Path) else image_path

    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise FileNotFoundError(f"Image not found at the path: {image_path}")

    if len(image.shape) == 2:  # Grayscale image
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGBA)
    elif image.shape[2] == 3:  # RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    elif image.shape[2] == 1:  # Grayscale
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGBA)
    elif image.shape[2] == 4:  # RGBA image, no need to convert
        pass

    if return_flipped:
        image = cv2.flip(image, 0)

    return image


def build_separator(orientation, parent=None):
    separator = qtw.QFrame(parent)
    if orientation == "horizontal":
        separator.setFrameShape(qtw.QFrame.Shape.HLine)
    elif orientation == "vertical":
        separator.setFrameShape(qtw.QFrame.Shape.VLine)
    else:
        raise ValueError("Invalid orientation: 'horizontal' or 'vertical' expected")

    separator.setFrameShadow(qtw.QFrame.Shadow.Sunken)
    return separator


class RangeIntValidator(qtg.QIntValidator):
    def __init__(self, lower_bound, upper_bound, parent=None):
        super(RangeIntValidator, self).__init__(lower_bound, upper_bound, parent)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def validate(self, input, pos):
        if input:
            try:
                value = int(input)
            except ValueError:
                return qtg.QValidator.State.Invalid, input, pos
            if self.lower_bound <= value <= self.upper_bound:
                return qtg.QIntValidator.State.Acceptable, input, pos
            else:
                return qtg.QIntValidator.State.Invalid, input, pos
        return qtg.QIntValidator.State.Intermediate, input, pos


class OpenGLGraphicsView(QOpenGLWidget):
    EPS = 1e-4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale_factor = 1.15
        self.min_scale = 1.0
        self.max_scale = 32
        self.current_scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.panning = False
        self.last_mouse_position = None
        self.texture_id = None
        self.texture_width = 0
        self.texture_height = 0

    def initializeGL(self):
        gl.glClearColor(0, 0, 0, 1)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # Always clear the screen
        if self.texture_id:
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)
            self.draw_image()
        else:
            gl.glLoadIdentity()

    def clamp_offsets(self):
        bound = self.current_scale - 1
        self.offset_x = max(-bound, min(bound, self.offset_x))
        self.offset_y = max(-bound, min(bound, self.offset_y))

    def draw_image(self):
        if self.texture_id is None:
            return

        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)

        self.clamp_offsets()

        # Apply transformations
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        # Translate for panning
        tx = self.offset_x  # / self.width()  # 2 * self.offset_x / self.width() - 1
        ty = self.offset_y  # / self.height()  # 2 * self.offset_y / self.height() - 1

        gl.glTranslatef(tx, ty, 0)

        # Scale the image
        gl.glScalef(self.current_scale, self.current_scale, 1)

        # Vertex and texture coordinates
        vertices = [-1, -1, 0, 1, -1, 0, 1, 1, 0, -1, 1, 0]
        tex_coords = [0, 0, 1, 0, 1, 1, 0, 1]

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, vertices)
        gl.glTexCoordPointer(2, gl.GL_FLOAT, 0, tex_coords)

        gl.glDrawArrays(gl.GL_QUADS, 0, 4)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        gl.glDisable(gl.GL_TEXTURE_2D)

    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Get the position of the mouse relative to the widget
            mouse_pos = event.position()
            scene_x_before = (mouse_pos.x() / self.width()) * 2 - 1 - self.offset_x
            scene_y_before = -((mouse_pos.y() / self.height()) * 2 - 1) - self.offset_y

            # Determine the scale direction
            if event.angleDelta().y() > 0 and self.current_scale < self.max_scale:
                new_scale = self.current_scale * self.scale_factor
            elif event.angleDelta().y() < 0 and self.current_scale > self.min_scale:
                new_scale = self.current_scale / self.scale_factor
            else:
                return  # No scaling to be done, exit early

            if new_scale <= self.min_scale + OpenGLGraphicsView.EPS:
                new_scale = self.min_scale
            if new_scale >= self.max_scale - OpenGLGraphicsView.EPS:
                new_scale = self.max_scale

            # new_scale = max(self.min_scale, min(self.max_scale, new_scale))

            # Calculate the new scene position after scaling
            scene_x_after = scene_x_before * (new_scale / self.current_scale)
            scene_y_after = scene_y_before * (new_scale / self.current_scale)

            # Update offsets to keep the mouse position stationary relative to the scene
            self.offset_x += scene_x_before - scene_x_after
            self.offset_y += scene_y_before - scene_y_after

            # Update the current scale
            self.current_scale = new_scale

            self.update()
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton and self.current_scale > 1:
            self.panning = True
            self.last_mouse_position = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self.panning:
            delta = event.position() - self.last_mouse_position
            self.last_mouse_position = event.position()
            self.offset_x += (delta.x() / self.width()) * 2 * 4 / 3 / self.current_scale
            self.offset_y -= (
                (delta.y() / self.height()) * 2 * 3 / 4 / self.current_scale
            )
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def load_image(self, image: np.ndarray):
        self.texture_height, self.texture_width, _ = image.shape

        # Generate a texture ID
        if self.texture_id is not None:
            gl.glDeleteTextures(1, [self.texture_id])
        self.texture_id = gl.glGenTextures(1)

        # Bind the texture ID
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)

        # Set the texture parameters
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)

        # Upload the texture data to GPU
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_RGBA,
            self.texture_width,
            self.texture_height,
            0,
            gl.GL_RGBA,
            gl.GL_UNSIGNED_BYTE,
            image,
        )

        # Unbind the texture
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def reset(self):
        self.current_scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.update()

    def clear_image(self):
        if self.texture_id:
            gl.glDeleteTextures(1, [self.texture_id])
            self.texture_id = None
        self.update()  # Request a repaint


class OpenGLImageViewer(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = OpenGLGraphicsView(self)
        self.error_label = qtw.QLabel()
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_image_label = qtw.QLabel()
        self.no_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.stacked_widget = qtw.QStackedWidget()
        self.stacked_widget.addWidget(self.view)
        self.stacked_widget.addWidget(self.error_label)
        self.stacked_widget.addWidget(self.no_image_label)

        self.setLayout(qtw.QVBoxLayout())
        self.layout().addWidget(self.stacked_widget)

        self.current_widget = None
        self._update_current_widget(self.no_image_label)

    def _update_current_widget(self, widget):
        if widget != self.current_widget:
            self.stacked_widget.setCurrentWidget(widget)
            self.current_widget = widget

    def set_image(self, image_path: Path):
        self.clear()

        if not Path(image_path).exists():
            self.error_label.setText(
                f"Image not found: {image_path}.\nPlease check if the file still exists or was renamed."
            )
            self._update_current_widget(self.error_label)
            return

        try:
            self._update_current_widget(self.view)
            image = open_image_as_rgb(image_path, return_flipped=True)
            self.view.load_image(image)
            self.view.update()
        except Exception as e:
            self.error_label.setText(
                f"Error loading image: {image_path}.\nPlease check if the file is a valid image.\n\nErrorMsg: {e}"
            )
            self._update_current_widget(self.error_label)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.current_widget == self.view:
            self.view.update()

    def clear(self):
        self._update_current_widget(self.no_image_label)
        if self.current_widget == self.view:
            self.view.clear_image()
            self.view.update()

    def set_keep_aspect_ratio(self, keep_aspect_ratio: bool):
        pass  # Not implemented
