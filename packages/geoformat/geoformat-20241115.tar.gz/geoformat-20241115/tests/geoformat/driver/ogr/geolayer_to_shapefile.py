from tests.data.geolayers import geolayer_attributes_only
from geoformat.conversion.fields_conversion import recast_field
from geoformat.driver.ogr.ogr_driver import geolayer_to_ogr_layer, ogr_layer_to_geolayer
from tests.geoformat.driver.ogr.compare_ogr_files import measure_time
from tests.utils.compare import compare_geolayer


def test_shapefile_attributes(attributes_geolayer):

    # recast field_binary to string (because ogr does not allow binary field in geojson format)
    attributes_geolayer = recast_field(
        geolayer_to_recast=attributes_geolayer,
        field_name_to_recast='field_integer_list',
        recast_to_geoformat_type='String',
        resize_width=254
    )

    attributes_geolayer = recast_field(
        geolayer_to_recast=attributes_geolayer,
        field_name_to_recast='field_real_list',
        recast_to_geoformat_type='String',
        resize_width=254
    )

    attributes_geolayer = recast_field(
        geolayer_to_recast=attributes_geolayer,
        field_name_to_recast='field_string_list',
        recast_to_geoformat_type='String',
        resize_width=254
    )

    attributes_geolayer = recast_field(
        geolayer_to_recast=attributes_geolayer,
        field_name_to_recast='field_time',
        recast_to_geoformat_type='String',
        resize_width=254
    )

    attributes_geolayer = recast_field(
        geolayer_to_recast=attributes_geolayer,
        field_name_to_recast='field_binary',
        recast_to_geoformat_type='String',
        resize_width=254
    )

    path_geolayer_attirbutes_only = 'data/geolayer_attributes_only.dbf'

    # write file
    geolayer_to_ogr_layer(
        geolayer=attributes_geolayer,
        path=path_geolayer_attirbutes_only,
        driver_name='esri shapefile'
    )

    # open created just bellow geojson to geolayer (to compare to geolayer_attributes_only)
    ogr_geolayer_attributes = ogr_layer_to_geolayer(path=path_geolayer_attirbutes_only)

    # compare both geolayer
    compare_geolayer(attributes_geolayer, ogr_geolayer_attributes)

if __name__ == '__main__':
    test_shapefile_attributes(attributes_geolayer=geolayer_attributes_only)