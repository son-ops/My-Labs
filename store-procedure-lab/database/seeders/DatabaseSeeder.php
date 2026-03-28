<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Employee;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        User::create([
            "name" => "admin",
            "email" => "admin@gmail.com",
            "password" => Hash::make('admin123')
        ]);
        User::factory(5)->create();
        Employee::factory(20)->create();
    }
}
