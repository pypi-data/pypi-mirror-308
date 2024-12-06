import math

from super_scad.boolean.Difference import Difference
from super_scad.boolean.Union import Union
from super_scad.d2.Polygon import Polygon
from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad.type.Angle import Angle
from super_scad_smooth_profile.SmoothProfile import SmoothProfile


class Chamfer(SmoothProfile):
    """
    Applies a chamfer to vertices at a node.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 skew_length: float | None = None,
                 skew_height: float | None = None,
                 inner_angle: float,
                 normal_angle: float,
                 position: Vector2,
                 child: ScadWidget):
        """
        Object constructor.

        :param skew_length: The length of the skew side of the chamfer.
        :param skew_height: The skew_height of the chamfer, measured perpendicular for the skew size to the node.
        :param inner_angle: Inner angle between the vertices.
        :param normal_angle: The normal angle of the vertices, i.e., the angle of the vector that lies exactly between
                             the two vertices and with origin at the node.
        :param child: The child object on which the fillet is applied.
        """
        SmoothProfile.__init__(self, args=locals(), child=child)

        self._validate_arguments()

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this profile.
        """
        admission = ArgumentAdmission(self._args)
        admission.validate_exclusive({'skew_length'}, {'skew_height'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def skew_height(self) -> float:
        """
        The skew_height of the chamfer, measured perpendicular for the skew size to the node.
        """
        if 'skew_height' in self._args:
            return self.uc(self._args['skew_height'])

        inner_angle = self.inner_angle
        if inner_angle > 180:
            inner_angle = 360.0 - inner_angle

        return 0.5 * self.skew_length / math.tan(math.radians(0.5 * inner_angle))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def skew_length(self) -> float:
        """
        The length of the skew side of the chamfer.
        """
        if 'skew_length' in self._args:
            return self.uc(self._args['skew_length'])

        inner_angle = self.inner_angle
        if inner_angle > 180:
            inner_angle = 360.0 - inner_angle

        return 2.0 * self.skew_height * math.tan(math.radians(0.5 * inner_angle))

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        if self.inner_angle < 180.0:
            # The corner is convex.
            polygon = self._build_polygon(context, self.normal_angle)

            return Difference(children=[self.child, polygon])

        if self.inner_angle > 180.0:
            # The corner is concave.
            polygon = self._build_polygon(context, Angle.normalize(self.normal_angle - 180.0))

            return Union(children=[self.child, polygon])

        return self.child

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon(self, context: Context, normal_angle: float) -> ScadWidget:
        """
        Returns a masking polygon.

        :param context: The build context.
        """
        p1 = self.position
        p2 = self.position + \
             Vector2.from_polar_coordinates(self.skew_height, normal_angle) + \
             Vector2.from_polar_coordinates(0.5 * self.skew_length, normal_angle + 90.0)
        p3 = p2 + Vector2.from_polar_coordinates(self.skew_length, normal_angle - 90.0)

        return Polygon(points=[p1, p2, p3], extend_sides_by_eps={0, 2})

# ----------------------------------------------------------------------------------------------------------------------
