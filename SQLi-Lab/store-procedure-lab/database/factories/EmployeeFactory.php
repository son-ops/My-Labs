<?php

namespace Database\Factories;

use App\Models\Employee;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Employee>
 */
class EmployeeFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'full_name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'department' => fake()->randomElement([
                'IT',
                'HR',
                'Finance',
                'Marketing',
                'Sales',
                'Operations',
            ]),
            'country' => fake()->randomElement([
                'Vietnam',
                'Japan',
                'Singapore',
                'Thailand',
                'USA',
                'Germany',
            ]),
            'salary_band' => fake()->randomElement(['10M', '15M', '20M'])
        ];
    }
}
