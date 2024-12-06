from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2

from super_scad_smooth_profile.Rough import Rough
from super_scad_smooth_profile.SmoothProfile import SmoothProfile
from super_scad_smooth_profile.SmoothProfileFactory import SmoothProfileFactory


class RoughFactory(SmoothProfileFactory):
    """
    A factory that produces rough smoothing profiles.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def create_smooth_profile(self,
                              *,
                              inner_angle: float,
                              normal_angle: float,
                              position: Vector2,
                              child: ScadWidget) -> SmoothProfile:
        """
        Returns a smoothing profile widget that applies no finishing.

        :param inner_angle: Inner angle between the vertices.
        :param normal_angle: The normal angle of the vertices, i.e., the angle of the vector that lies exactly between
                             the two vertices and with origin at the node.
        :param position: The position of the node.
        :param child: The child object on which the smoothing must be applied.
        """
        return Rough(child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def offset1(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the first vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        return 0.0

    # ------------------------------------------------------------------------------------------------------------------
    def offset2(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the second vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        return 0.0

# ----------------------------------------------------------------------------------------------------------------------
