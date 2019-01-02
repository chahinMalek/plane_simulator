from bintrees import AVLTree as AVL

from objects.geometric_objects import Circle, Point2

points = [
    Point2(-6, 3),
    Point2(-5, 2),
    Point2(4.72, 2.01),
    Point2(-4.24, 6.33),
    Point2(-2, 4),
    Point2(-1.76, -3.15),
    Point2(-1.4, -1.19),
    Point2(4.76, 3.69),
]

circles = [Circle(center=x, radius=1) for x in points]

start_points_map = {}
end_points_map = {}

for index, circle in enumerate(circles):
    start_points_map[(circle.center.x - circle.radius, circle.center.y)] = index
    end_points_map[(circle.center.x + circle.radius, circle.center.y)] = index

event_points = [x for x in start_points_map.keys()]
event_points.extend(x for x in end_points_map.keys())
event_points.sort()

start_points = sorted(start_points_map.keys(), reverse=True)
end_points = sorted(end_points_map.keys(), reverse=True)

tree = AVL()

while len(start_points) > 0 and len(end_points) > 0:

    if start_points[-1] <= end_points[-1]:
        circle = circles[start_points_map[start_points[-1]]]
        tree.insert(circle.center, circle)

        try:
            key = circle.center

            while True:
                prev = tree.prev_item(key)[1]

                if prev.intersects(circle):
                    print('Intersection found: {} and {}'.format(prev, circle))
                key = prev.center

        except KeyError:
            pass

        try:
            key = circle.center

            while True:
                prev = tree.succ_item(key)[1]

                if prev.intersects(circle):
                    print('Intersection found: {} and {}'.format(prev, circle))
                key = prev.center

        except KeyError:
            pass

        start_points.pop()

    else:
        tree.remove(circles[end_points_map[end_points[-1]]].center)
        end_points.pop()


while len(end_points) > 0:
    tree.remove(circles[end_points_map[end_points[-1]]].center)
    end_points.pop()
