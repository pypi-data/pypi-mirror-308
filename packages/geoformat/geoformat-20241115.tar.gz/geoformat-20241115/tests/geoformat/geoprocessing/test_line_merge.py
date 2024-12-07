from tests.utils.tests_utils import test_function

from geoformat.geoprocessing.line_merge import line_merge

line_merge_parameters = {
    0: {
        "geometry": {"type": "LineString", "coordinates": []},
        "bbox": False,
        "return_value": {"type": "LineString", "coordinates": []}
    },
    1: {
        "geometry": {"type": "MultiLineString", "coordinates": []},
        "bbox": False,
        "return_value": {"type": "MultiLineString", "coordinates": []}
    },
    2: {
        "geometry": {"type": "GeometryCollection", "geometries": []},
        "bbox": False,
        "return_value": {"type": "GeometryCollection", "geometries": []}
    },
    3: {
        "geometry":
            {"type": "MultiLineString",
             "coordinates": [
                [[2, 8], [4, 6]],
                [[4, 2], [7, 6]],
                [[4, 2], [4, 6]],
                [[2, 8], [1, 4]],
                [[6, 0], [4, 2]],
                [[10, 3], [7, 6]],
                [[5, 10], [7, 8]],
                [[7, 8], [9, 10]],
            ],
        },
        "bbox": False,
        "return_value": {"type":"MultiLineString","coordinates": [[[1, 4], [2, 8], [4, 6], [4, 2]], [[5, 10], [7, 8], [9, 10]], [[4, 2], [7, 6], [10, 3]], [[6, 0], [4, 2]]]}
    },
    4: {
        "geometry": { #  ring with 4 parts
            "type": "MultiLineString",
            "coordinates": [
                [[2, 3], [5, 2], [8, 4]],
                [[5, 9], [3, 6]],
                [[3, 6], [2, 3]],
                [[8, 4], [9, 7], [5, 9]],
            ],
        },
        "bbox": False,
        "return_value": {"type": "LineString", "coordinates": [[8, 4], [9, 7], [5, 9], [3, 6], [2, 3], [5, 2], [8, 4]]}
    },
    5: {
        "geometry": { # loop ring in 2 parts
            "type": "MultiLineString",
            "coordinates": [
                [[3, 6], [2, 3], [5, 2], [8, 4]],
                [[8, 4], [9, 7], [5, 9], [3, 6]],
            ],
        },
        "bbox": False,
        "return_value": {"type": "LineString", "coordinates": [[8, 4], [9, 7], [5, 9], [3, 6], [2, 3], [5, 2], [8, 4]]}
    },
    6: {
        "geometry": { # loop ring but cancelled by a third part (at point [5, 2])
            "type": "MultiLineString",
            "coordinates": [
                [[3, 6], [2, 3], [5, 2], [8, 4]],
                [[8, 4], [9, 7], [5, 9], [3, 6]],
                [[5, 2], [0, 0]],
            ],
        },
        "bbox": False,
        "return_value": {"type":"MultiLineString","coordinates": [[[8, 4], [9, 7], [5, 9], [3, 6], [2, 3], [5, 2], [8, 4]], [[5, 2], [0, 0]]]}
    },
    7: {
        "geometry": { # loop ring with 2 parts but cancelled by a third part (at point [5, 2])
                      # with duplicated other part
            "type": "MultiLineString",
            "coordinates": [
                [[3, 6], [2, 3], [5, 2], [8, 4]],
                [[8, 4], [9, 7], [5, 9], [3, 6]],
                [[5, 2], [0, 0]],
                [[3, 6], [2, 3], [5, 2], [8, 4]],  # duplicate part
                [[8, 4], [9, 7], [5, 9], [3, 6]],  # duplicate part
                [[5, 2], [0, 0]],  # duplicate part
            ],
        },
        "bbox": False,
        "return_value": {"type":"MultiLineString","coordinates": [[[0, 0], [5, 2], [0, 0]], [[3, 6], [2, 3], [5, 2], [8, 4]], [[8, 4], [9, 7], [5, 9], [3, 6]], [[3, 6], [2, 3], [5, 2], [8, 4]], [[8, 4], [9, 7], [5, 9], [3, 6]]]}
    },
    8: {
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [438589.8, 6789320.8],
                [438565.2, 6789230.3],
                [438550.0, 6789190.5],
                [438519.7, 6789145.7],
                [438479.5, 6789106.1],
                [438477.2, 6789075.9],
                [438477.2, 6789075.9],
            ],
        },
        "bbox": False,
        "return_value": {
            "type": "LineString",
            "coordinates": [
                [438589.8, 6789320.8], [438565.2, 6789230.3], [438550.0, 6789190.5], [438519.7, 6789145.7], [438479.5, 6789106.1], [438477.2, 6789075.9]
            ]
        }
    },
    9: {
        "geometry": {
            "type": "MultiLineString",
            "coordinates": [
                [
                    [650942.200000008, 6857645.800000944],
                    [645325.1000000088, 6859675.200000941],
                    [645325.1000000088, 6859675.200000941],
                    [643644.0000000091, 6863500.900000929],
                ],
                [
                    [670055.5000000049, 6856451.100000947],
                    [671600.3000000048, 6851282.800000963],
                    [671600.3000000048, 6851282.800000963],
                ],
                [
                    [799606.7999999593, 6263118.800002612],
                    [799606.7999999593, 6263118.800002612],
                    [825917.6999999485, 6262029.800002615],
                ],
                [
                    [869889.3999999303, 6258065.200002626],
                    [869889.3999999303, 6258065.200002626],
                    [866898.8999999315, 6258271.7000026265],
                    [866898.8999999315, 6258271.7000026265],
                    [866898.8999999315, 6258271.7000026265],
                    [866104.2999999323, 6264876.400002609],
                    [862373.7999999337, 6265459.30000261],
                    [862373.7999999337, 6265459.30000261],
                    [862373.7999999337, 6265459.30000261],
                    [862373.7999999337, 6265459.30000261],
                ],
            ],
        },
        "bbox": False,
        "return_value": {
            "type": "MultiLineString",
            "coordinates": [
                [[650942.200000008, 6857645.800000944], [645325.1000000088, 6859675.200000941], [643644.0000000091, 6863500.900000929]], [[670055.5000000049, 6856451.100000947], [671600.3000000048, 6851282.800000963]], [[799606.7999999593, 6263118.800002612], [825917.6999999485, 6262029.800002615]], [[869889.3999999303, 6258065.200002626], [866898.8999999315, 6258271.7000026265], [866104.2999999323, 6264876.400002609], [862373.7999999337, 6265459.30000261]]
            ]}
    },
    10: {
        "geometry": {"type": "MultiLineString", "coordinates": [
            [[-3, 6], [-2, 4], [-2, 2]],
            [[-3, 6], [-2, 4]],
            [[-2, 4], [-2, 2]]
        ]},
        "bbox": False,
        "return_value": {"type": "LineString", "coordinates": [[-2, 2], [-2, 4], [-3, 6], [-2, 4], [-2, 2]]}
    },
    11: {
        "geometry": {"type": "GeometryCollection", "geometries": [{"type": "MultiLineString", "coordinates": [[[-3, 6], [-2, 4], [-2, 2]], [[-3, 6], [-2, 4]], [[-2, 4], [-2, 2]]]}, {"type": "LineString", "coordinates": [[438589.8, 6789320.8], [438565.2, 6789230.3], [438550.0, 6789190.5], [438519.7, 6789145.7], [438479.5, 6789106.1], [438477.2, 6789075.9], [438477.2, 6789075.9]]}, {"type": "Polygon", "coordinates": []}, {"type": "Point", "coordinates": [[3456687, 978956]]}]},
        "bbox": False,
        "return_value": {"type": "GeometryCollection", "geometries": [{"type": "LineString", "coordinates": [[-2, 2], [-2, 4], [-3, 6], [-2, 4], [-2, 2]]}, {'type': 'LineString', 'coordinates': [[438589.8, 6789320.8], [438565.2, 6789230.3], [438550.0, 6789190.5], [438519.7, 6789145.7], [438479.5, 6789106.1], [438477.2, 6789075.9]]}, {"type": "Polygon", "coordinates": []}, {"type": "Point", "coordinates": [[3456687, 978956]]}]}
    },
    12: {
        "geometry": {"type": "LineString", "coordinates": []},
        "bbox": True,
        "return_value": {"type":"LineString", "coordinates": []}
    },
    13: {
        "geometry": {"type": "MultiLineString", "coordinates": []},
        "bbox": True,
        "return_value": {"type":"MultiLineString","coordinates":[]}
    },
    14: {
        "geometry": {"type": "GeometryCollection", "geometries": []},
        "bbox": True,
        "return_value": {"type":"GeometryCollection","geometries":[]}
    },
    15: {
        "geometry":
            {"type": "MultiLineString",
             "coordinates": [
                [[2, 8], [4, 6]],
                [[4, 2], [7, 6]],
                [[4, 2], [4, 6]],
                [[2, 8], [1, 4]],
                [[6, 0], [4, 2]],
                [[10, 3], [7, 6]],
                [[5, 10], [7, 8]],
                [[7, 8], [9, 10]],
            ]
        },
        "bbox": True,
        "return_value": {"type": "MultiLineString",
                         "coordinates": [[[1, 4], [2, 8], [4, 6], [4, 2]], [[5, 10], [7, 8], [9, 10]], [[4, 2], [7, 6], [10, 3]], [[6, 0], [4, 2]]],
                         "bbox": (1, 0, 10, 10)}
    },
    16: {
        "geometry": { #  ring with 4 parts
            "type": "MultiLineString",
            "coordinates": [
                [[2, 3], [5, 2], [8, 4]],
                [[5, 9], [3, 6]],
                [[3, 6], [2, 3]],
                [[8, 4], [9, 7], [5, 9]],
            ]
        },
        "bbox": True,
        "return_value": {"type": "LineString",
                         "coordinates": [[8, 4], [9, 7], [5, 9], [3, 6], [2, 3], [5, 2], [8, 4]],
                         'bbox': (2, 2, 9, 9)
        }
    },
    17: {
        "geometry": { # loop ring in 2 parts
            "type": "MultiLineString",
            "coordinates": [
                [[3, 6], [2, 3], [5, 2], [8, 4]],
                [[8, 4], [9, 7], [5, 9], [3, 6]],
            ]
        },
        "bbox": True,
        "return_value": {"type": "LineString",
                         "coordinates": [[8, 4], [9, 7], [5, 9], [3, 6], [2, 3], [5, 2], [8, 4]],
                         'bbox': (2, 2, 9, 9)
        }
    },
    18: {
        "geometry": { # loop ring but cancelled by a third part (at point [5, 2])
            "type": "MultiLineString",
            "coordinates": [
                [[3, 6], [2, 3], [5, 2], [8, 4]],
                [[8, 4], [9, 7], [5, 9], [3, 6]],
                [[5, 2], [0, 0]],
            ],
        },
        "bbox": True,
        "return_value": {
            "type": "MultiLineString",
            "coordinates": [[[8, 4], [9, 7], [5, 9], [3, 6], [2, 3], [5, 2], [8, 4]], [[5, 2], [0, 0]]],
            'bbox': (0, 0, 9, 9)
        }
    },
    19: {
        "geometry": { # loop ring with 2 parts but cancelled by a third part (at point [5, 2])
                      # with duplicated other part
            "type": "MultiLineString",
            "coordinates": [
                [[3, 6], [2, 3], [5, 2], [8, 4]],
                [[8, 4], [9, 7], [5, 9], [3, 6]],
                [[5, 2], [0, 0]],
                [[3, 6], [2, 3], [5, 2], [8, 4]],  # duplicate part
                [[8, 4], [9, 7], [5, 9], [3, 6]],  # duplicate part
                [[5, 2], [0, 0]],  # duplicate part
            ],
        },
        "bbox": True,
        "return_value": {"type":"MultiLineString", "coordinates": [[[0, 0], [5, 2], [0, 0]], [[3, 6], [2, 3], [5, 2], [8, 4]], [[8, 4], [9, 7], [5, 9], [3, 6]], [[3, 6], [2, 3], [5, 2], [8, 4]], [[8, 4], [9, 7], [5, 9], [3, 6]]], 'bbox': (0, 0, 9, 9)}
    },
    20: {
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [438589.8, 6789320.8],
                [438565.2, 6789230.3],
                [438550.0, 6789190.5],
                [438519.7, 6789145.7],
                [438479.5, 6789106.1],
                [438477.2, 6789075.9],
                [438477.2, 6789075.9],
            ],
        },
        "bbox": True,
        "return_value": {
            "type": "LineString",
            "coordinates": [
                [438589.8, 6789320.8], [438565.2, 6789230.3], [438550.0, 6789190.5], [438519.7, 6789145.7], [438479.5, 6789106.1], [438477.2, 6789075.9]
            ],
            "bbox": (438477.2, 6789075.9, 438589.8, 6789320.8)
        }
    },
    21: {
        "geometry": {
            "type": "MultiLineString",
            "coordinates": [
                [
                    [650942.200000008, 6857645.800000944],
                    [645325.1000000088, 6859675.200000941],
                    [645325.1000000088, 6859675.200000941],
                    [643644.0000000091, 6863500.900000929],
                ],
                [
                    [670055.5000000049, 6856451.100000947],
                    [671600.3000000048, 6851282.800000963],
                    [671600.3000000048, 6851282.800000963],
                ],
                [
                    [799606.7999999593, 6263118.800002612],
                    [799606.7999999593, 6263118.800002612],
                    [825917.6999999485, 6262029.800002615],
                ],
                [
                    [869889.3999999303, 6258065.200002626],
                    [869889.3999999303, 6258065.200002626],
                    [866898.8999999315, 6258271.7000026265],
                    [866898.8999999315, 6258271.7000026265],
                    [866898.8999999315, 6258271.7000026265],
                    [866104.2999999323, 6264876.400002609],
                    [862373.7999999337, 6265459.30000261],
                    [862373.7999999337, 6265459.30000261],
                    [862373.7999999337, 6265459.30000261],
                    [862373.7999999337, 6265459.30000261],
                ],
            ],
        },
        "bbox": True,
        "return_value": {
            "type": "MultiLineString",
            "coordinates": [
                [[650942.200000008, 6857645.800000944], [645325.1000000088, 6859675.200000941], [643644.0000000091, 6863500.900000929]], [[670055.5000000049, 6856451.100000947], [671600.3000000048, 6851282.800000963]], [[799606.7999999593, 6263118.800002612], [825917.6999999485, 6262029.800002615]], [[869889.3999999303, 6258065.200002626], [866898.8999999315, 6258271.7000026265], [866104.2999999323, 6264876.400002609], [862373.7999999337, 6265459.30000261]]
            ],
            'bbox': (643644.0000000091, 6258065.200002626, 869889.3999999303, 6863500.900000929)
        }
    },
    22: {
        "geometry": {"type": "MultiLineString", "coordinates": [[[-3, 6], [-2, 4], [-2, 2]], [[-3, 6], [-2, 4]], [[-2, 4], [-2, 2]]]},
        "bbox": True,
        "return_value": {"type": "LineString", "coordinates": [[-2, 2], [-2, 4], [-3, 6], [-2, 4], [-2, 2]], 'bbox': (-3, 2, -2, 6)}
    },
    23: {
        "geometry": {"type": "GeometryCollection",
                     "geometries": [
                         {"type": "MultiLineString", "coordinates": [[[-3, 6], [-2, 4], [-2, 2]], [[-3, 6], [-2, 4]], [[-2, 4], [-2, 2]]]},
                         {"type": "LineString", "coordinates": [[438589.8, 6789320.8], [438565.2, 6789230.3], [438550.0, 6789190.5], [438519.7, 6789145.7], [438479.5, 6789106.1], [438477.2, 6789075.9], [438477.2, 6789075.9]]},
                         {"type": "Polygon", "coordinates": []},
                         {"type": "Point", "coordinates": [[3456687, 978956]]}
                     ]
                     },
        "bbox": True,
        "return_value": {"type": "GeometryCollection",
                         "geometries": [
                             {"type": "LineString", "coordinates": [[-2, 2], [-2, 4], [-3, 6], [-2, 4], [-2, 2]], 'bbox': (-3, 2, -2, 6)},
                             {'type': 'LineString', 'coordinates': [[438589.8, 6789320.8], [438565.2, 6789230.3], [438550.0, 6789190.5], [438519.7, 6789145.7], [438479.5, 6789106.1], [438477.2, 6789075.9]], 'bbox': (438477.2, 6789075.9, 438589.8, 6789320.8)},
                             {"type": "Polygon", "coordinates": []},
                             {"type": "Point", "coordinates": [[3456687, 978956]], 'bbox': (3456687, 978956, 3456687, 978956)}
                         ],
                         "bbox": (-3, 2, 3456687, 6789320.8)}
    },
    24: {
        "geometry":
            {"type": "MultiLineString",
             "coordinates": [
                 [[2, 8], [4, 6]],
                 [[4, 2], [7, 6]],
                 [[4, 2], [4, 6]],
                 [[2, 8], [1, 4]],
                 [[6, 0], [4, 2]],
                 [[10, 3], [7, 6]],
                 [[5, 10], [7, 8]],
                 [[7, 8], [9, 10]],
             ],
             },
        "directed": True,
        "bbox": False,
        "return_value": {"type": "MultiLineString",
                         "coordinates": [[[5, 10], [7, 8], [9, 10]], [[2, 8], [4, 6]], [[4, 2], [7, 6]], [[4, 2], [4, 6]], [[2, 8], [1, 4]], [[6, 0], [4, 2]], [[10, 3], [7, 6]]]}

    },
    25: {
        "geometry": {  # ring with 4 parts
            "type": "MultiLineString",
            "coordinates": [
                [[2, 3], [5, 2], [8, 4]],
                [[5, 9], [3, 6]],
                [[3, 6], [2, 3]],
                [[8, 4], [9, 7], [5, 9]],
            ],
        },
        "directed": True,
        "bbox": False,
        "return_value": {"type": "LineString", "coordinates": [[8, 4], [9, 7], [5, 9], [3, 6], [2, 3], [5, 2], [8, 4]]}
    },
    26: {
        "geometry": {  # loop ring in 2 parts
            "type": "MultiLineString",
            "coordinates": [
                [[3, 6], [2, 3], [5, 2], [8, 4]],
                [[8, 4], [9, 7], [5, 9], [3, 6]],
            ],
        },
        "bbox": False,
        "directed": True,
        "return_value": {"type": "LineString", "coordinates": [[8, 4], [9, 7], [5, 9], [3, 6], [2, 3], [5, 2], [8, 4]]}
    },
    27: {
        "geometry": { # loop ring but cancelled by a third part (at point [5, 2])
            "type": "MultiLineString",
            "coordinates": [
                [[3, 6], [2, 3], [5, 2], [8, 4]],
                [[8, 4], [9, 7], [5, 9], [3, 6]],
                [[5, 2], [0, 0]],
            ],
        },
        "directed": True,
        "bbox": False,
        "return_value": {
            "type": "MultiLineString",
            "coordinates": [[[8, 4], [9, 7], [5, 9], [3, 6], [2, 3], [5, 2], [8, 4]], [[5, 2], [0, 0]]],
        },
    },
    28: {
        "geometry": {  # loop ring with 2 parts but cancelled by a third part (at point [5, 2])
            # with duplicated other part
            "type": "MultiLineString",
            "coordinates": [
                [[3, 6], [2, 3], [5, 2], [8, 4]],
                [[8, 4], [9, 7], [5, 9], [3, 6]],
                [[5, 2], [0, 0]],
                [[3, 6], [2, 3], [5, 2], [8, 4]],  # duplicate part
                [[8, 4], [9, 7], [5, 9], [3, 6]],  # duplicate part
                [[5, 2], [0, 0]],  # duplicate part
            ],
        },
        "directed": True,
        "bbox": False,
        "return_value": {"type": "MultiLineString",
                         "coordinates": [[[3, 6], [2, 3], [5, 2], [8, 4]], [[8, 4], [9, 7], [5, 9], [3, 6]], [[5, 2], [0, 0]], [[3, 6], [2, 3], [5, 2], [8, 4]], [[8, 4], [9, 7], [5, 9], [3, 6]], [[5, 2], [0, 0]]]}
    },
    29: {
        "geometry": {"type": "MultiLineString", "coordinates": [
            [[-3, 6], [-2, 4], [-2, 2]],
            [[-3, 6], [-2, 4]],
            [[-2, 4], [-2, 2]]
        ]},
        "directed": True,
        "bbox": False,
        "return_value": {'type': 'MultiLineString', 'coordinates': [[[-3, 6], [-2, 4], [-2, 2]], [[-3, 6], [-2, 4], [-2, 2]]]}
    },
    30: {
        "geometry": {"type": "MultiLineString", "coordinates": [
            [[0, 0], [0, 10], [-10, 10]],
            [[0, 10], [0, 0]],
            [[0, 0], [-10, 0]]
        ]},
        "directed": False,
        "bbox": False,
        "return_value": {'type': 'MultiLineString', 'coordinates':  [[[0, 0], [0, 10], [-10, 10]], [[0, 10], [0, 0]], [[0, 0], [-10, 0]]]}
    },
    31: {
        "geometry": {"type": "MultiLineString", "coordinates": [
            [[0, 0], [0, 10], [-10, 10]],
            [[0, 10], [0, 0]],
            [[0, 0], [-10, 0]]
        ]},
        "directed": True,
        "bbox": False,
        "return_value": {'type': 'MultiLineString', 'coordinates':  [[[0, 0], [0, 10], [-10, 10]], [[0, 10], [0, 0]], [[0, 0], [-10, 0]]]}
    }
}


def test_all():
    # line merge
    print(test_function(line_merge, line_merge_parameters))

if __name__ == '__main__':
    test_all()
