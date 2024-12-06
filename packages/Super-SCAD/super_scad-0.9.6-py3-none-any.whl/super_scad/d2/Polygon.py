from typing import List, Set

from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.d2.private.PrivatePolygon import PrivatePolygon
from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Vector2 import Vector2


class Polygon(PolygonMixin, ScadWidget):
    """
    Widget for creating polygons. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#polygon.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 primary: List[Vector2] | None = None,
                 points: List[Vector2] | None = None,
                 secondary: List[Vector2] | None = None,
                 secondaries: List[List[Vector2]] | None = None,
                 convexity: int | None = None,
                 extend_sides_by_eps: bool | List[bool] | Set[int] | None = None,
                 delta: float | None = None):
        """
        Object constructor.

        :param primary: The list of 2D points of the polygon.
        :param points: Alias for primary.
        :param secondary: The secondary path that will be subtracted from the polygon.
        :param secondaries: The secondary paths that will be subtracted form the polygon.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line
                          through the child widget.
        :param extend_sides_by_eps: Whether to extend sides by eps for a clear overlap.
        :param delta: The minimum distance between nodes, vertices and line segments for reliable computation of the
                      separation between line segments and nodes.
        """
        ScadWidget.__init__(self, args=locals())
        PolygonMixin.__init__(self, extend_sides_by_eps=extend_sides_by_eps, delta=delta)

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        admission = ArgumentAdmission(self._args)
        admission.validate_exclusive({'primary'}, {'points'})
        admission.validate_exclusive({'secondary'}, {'secondaries'})
        admission.validate_required({'primary', 'points'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def primary(self) -> List[Vector2]:
        """
        Returns the points of the polygon.
        """
        return self.uc(self._args.get('primary', self._args.get('points')))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def secondaries(self) -> List[List[Vector2]] | None:
        """
        Returns the points of the polygon.
        """
        if 'secondaries' in self._args:
            return [self.uc(point) for point in self._args.get('secondaries')]

        if 'secondary' in self._args:
            return [self.uc(self._args['secondary'])]

        return None

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def nodes(self) -> List[Vector2]:
        """
        Returns the nodes of the polygon.
        """
        return self.primary

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        secondaries = self.secondaries
        if secondaries is None:
            return PrivatePolygon(points=self.primary, convexity=self.convexity)

        points = self.primary
        n = 0
        m = n + len(points)
        paths = [list(range(n, m))]
        n = m

        for secondary in secondaries:
            m = n + len(secondary)
            points += secondary
            paths.append(list(range(n, m)))
            n = m

        return PrivatePolygon(points=points, paths=paths, convexity=self.convexity)

# ----------------------------------------------------------------------------------------------------------------------
