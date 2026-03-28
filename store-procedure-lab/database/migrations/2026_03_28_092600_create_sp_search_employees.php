<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    public function up(): void
    {
        DB::unprepared(<<<'SQL'
DROP PROCEDURE IF EXISTS sp_search_employees;
CREATE PROCEDURE sp_search_employees(
    IN p_keyword VARCHAR(100),
    IN p_department VARCHAR(50),
    IN p_country VARCHAR(50),
    IN p_view_mode VARCHAR(30),
    IN p_sort_mode VARCHAR(255)
)
BEGIN
    DECLARE v_cols TEXT;
    DECLARE v_order TEXT;

    SET v_cols = CASE p_view_mode
        WHEN 'basic' THEN 'id, full_name, email, department, country'
        WHEN 'hr' THEN 'id, full_name, email, department, country, salary_band, created_at'
        WHEN 'manager' THEN 'id, full_name, email, department, country, salary_band'
        ELSE 'id, full_name, email, department, country'
    END;

    SET v_order = CASE p_sort_mode
        WHEN 'name_asc' THEN 'full_name ASC'
        WHEN 'name_desc' THEN 'full_name DESC'
        WHEN 'department_asc' THEN 'department ASC, full_name ASC'
        WHEN 'newest' THEN 'created_at DESC'
        WHEN 'oldest' THEN 'created_at ASC'
        ELSE p_sort_mode
    END;

    SET @sql = CONCAT(
        'SELECT ', v_cols, '
         FROM employees
         WHERE (? = '''' OR full_name LIKE CONCAT(''%'', ?, ''%'') OR email LIKE CONCAT(''%'', ?, ''%'')) 
           AND (? = '''' OR department = ?)
           AND (? = '''' OR country = ?)
         ORDER BY ', v_order, '
         LIMIT 50'
    );

    PREPARE stmt FROM @sql;

    SET @kw1 = COALESCE(p_keyword, '');
    SET @kw2 = COALESCE(p_keyword, '');
    SET @kw3 = COALESCE(p_keyword, '');

    SET @dep1 = COALESCE(p_department, '');
    SET @dep2 = COALESCE(p_department, '');

    SET @country1 = COALESCE(p_country, '');
    SET @country2 = COALESCE(p_country, '');

    EXECUTE stmt USING
        @kw1, @kw2, @kw3,
        @dep1, @dep2,
        @country1, @country2;

    DEALLOCATE PREPARE stmt;
END
SQL);
    }

    public function down(): void
    {
        DB::unprepared('DROP PROCEDURE IF EXISTS sp_search_employees');
    }
};