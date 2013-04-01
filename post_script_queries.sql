-- Borrar el campo custom que ya no nos sirve
DELETE FROM package_extra_revision WHERE continuity_id IN (SELECT id FROM package_extra WHERE key='category');
DELETE FROM package_extra WHERE key='category';

-- Sacar comillas dobles innecesarias en los valores de frec. de actualizacion
UPDATE package_extra SET value=replace(value,'"','') WHERE key='update_frequency';
