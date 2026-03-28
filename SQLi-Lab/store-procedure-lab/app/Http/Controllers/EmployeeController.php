<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class EmployeeController extends Controller
{
    public function index()
    {
        return view('employees.index');
    }

    public function search(Request $request)
    {
        $data = $request->validate([
            'keyword' => 'nullable|string|max:100',
            'department' => 'nullable|string|max:50',
            'country' => 'nullable|string|max:50',
            'view_mode' => 'required|string|max:30',
            'sort_mode' => 'required|string|max:100',
        ]);

        $rows = DB::select('CALL sp_search_employees(?,?,?,?,?)', [
            $data['keyword'] ?? '',
            $data['department'] ?? '',
            $data['country'] ?? '',
            $data['view_mode'],
            $data['sort_mode'],
        ]);

        return view('employees.index', compact('rows'));
    }
}