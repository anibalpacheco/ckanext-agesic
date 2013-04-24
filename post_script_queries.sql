-- Borrar el campo custom que ya no nos sirve
DELETE FROM package_extra_revision WHERE continuity_id IN (SELECT id FROM package_extra WHERE key='category');
DELETE FROM package_extra WHERE key='category';

-- Sacar comillas dobles innecesarias en los valores de frec. de actualizacion
UPDATE package_extra SET value=replace(value,'"','') WHERE key='update_frequency';

-- Homogeneizar los demás campos custom
UPDATE package_extra SET key='spatial_ref_system' WHERE lower(trim(key))='sistema de referencia';
UPDATE package_extra_revision SET key='spatial_ref_system' WHERE lower(trim(key))='sistema de referencia';
UPDATE package_extra SET key='spatial_coverage' WHERE lower(trim(key))~'co[bv]ertura espacial';
UPDATE package_extra_revision SET key='spatial_coverage' WHERE lower(trim(key))~'co[bv]ertura espacial';
UPDATE package_extra SET key='temporal_coverage' WHERE lower(trim(key))~'co[bv]ertura temporal';
UPDATE package_extra_revision SET key='temporal_coverage' WHERE lower(trim(key))~'co[bv]ertura temporal';
