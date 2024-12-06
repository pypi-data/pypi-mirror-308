import math

from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad_smooth_profile.SmoothProfile import SmoothProfile
from super_scad_smooth_profile.SmoothProfileFactory import SmoothProfileFactory

from super_scad_smooth_profiles.Fillet import Fillet


class FilletFactory(SmoothProfileFactory):
    """
    A factory that produces fillet smoothing profiles.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, radius: float):
        """
        Object constructor.

        :param radius: The radius of the fillet.
        """
        self._radius = radius
        """
        The radius of the fillet.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def offset1(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the first vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        if self._radius > 0.0 and inner_angle < 180.0:
            # The corner is convex.
            alpha = math.radians(inner_angle) / 2.0

            return self._radius * math.cos(alpha) / math.sin(alpha)

        if self._radius > 0.0 and inner_angle > 180.0:
            # The corner is concave.
            alpha = math.radians(360.0 - inner_angle) / 2.0

            return self._radius * math.cos(alpha) / math.sin(alpha)

        if self._radius < 0.0:
            # Negative radius.
            return self._radius

        return 0.0

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
        Returns a smoothing profile widget creating a fillet.

        :param inner_angle: Inner angle between the vertices.
        :param normal_angle: The normal angle of the vertices, i.e., the angle of the vector that lies exactly between
                             the two vertices and with origin at the node.
        :param position: The position of the node.
        :param child: The child object on which the smoothing must be applied.
        """
        return Fillet(radius=self._radius,
                      inner_angle=inner_angle,
                      normal_angle=normal_angle,
                      position=position,
                      child=child)

# ----------------------------------------------------------------------------------------------------------------------
