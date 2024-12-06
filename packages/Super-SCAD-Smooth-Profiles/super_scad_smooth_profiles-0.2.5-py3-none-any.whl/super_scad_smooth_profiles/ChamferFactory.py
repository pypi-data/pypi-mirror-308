import math

from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad_smooth_profile.SmoothProfile import SmoothProfile
from super_scad_smooth_profile.SmoothProfileFactory import SmoothProfileFactory

from super_scad_smooth_profiles.Chamfer import Chamfer


class ChamferFactory(SmoothProfileFactory):
    """
    A factory that produces chamfer smoothing profiles.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 skew_length: float | None = None,
                 skew_height: float | None = None):
        """
        Object constructor.

        :param skew_length: The length of the skew side of the chamfer.
        :param skew_height: The skew_height of the chamfer, measured perpendicular for the skew size to the node.
        """
        self._skew_length: float = skew_length
        """
        The length of the chamfer.
        """

        self._skew_height: float = skew_height
        """
        The height of the chamfer.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def skew_height(self, *, inner_angle: float) -> float:
        """
        The skew_height of the chamfer, measured perpendicular for the skew size to the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        if self._skew_height is not None:
            return self._skew_height

        if inner_angle > 180:
            inner_angle = 360.0 - inner_angle

        return 0.5 * self._skew_length / math.tan(math.radians(0.5 * inner_angle))

    # ------------------------------------------------------------------------------------------------------------------
    def skew_length(self, *, inner_angle: float) -> float:
        """
        The length of the skew side of the chamfer.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        if self._skew_length is not None:
            return self._skew_length

        if inner_angle > 180:
            inner_angle = 360.0 - inner_angle

        return 2.0 * self._skew_height * math.tan(math.radians(0.5 * inner_angle))

    # ------------------------------------------------------------------------------------------------------------------
    def offset1(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the first vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        if inner_angle > 180:
            inner_angle = 360.0 - inner_angle

        return self.skew_height(inner_angle=inner_angle) / math.cos(math.radians(0.5 * inner_angle))

    # ------------------------------------------------------------------------------------------------------------------
    def offset2(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the second vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        return self.offset1(inner_angle=inner_angle)

    # ------------------------------------------------------------------------------------------------------------------
    def create_smooth_profile(self,
                              *,
                              inner_angle: float,
                              normal_angle: float,
                              position: Vector2,
                              child: ScadWidget) -> SmoothProfile:
        """
        Returns a smoothing profile widget creating a chamfer.

        :param inner_angle: Inner angle between the vertices.
        :param normal_angle: The normal angle of the vertices, i.e., the angle of the vector that lies exactly between
                             the two vertices and with origin at the node.
        :param position: The position of the node.
        :param child: The child object on which the smoothing must be applied.
        """
        return Chamfer(skew_length=self._skew_length,
                       skew_height=self._skew_height,
                       inner_angle=inner_angle,
                       normal_angle=normal_angle,
                       position=position,
                       child=child)

# ----------------------------------------------------------------------------------------------------------------------
