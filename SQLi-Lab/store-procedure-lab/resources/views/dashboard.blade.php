<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 leading-tight">
            {{ __('Dashboard') }}
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8 space-y-6">
            
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6 text-gray-900">
                    {{ __("You're logged in!") }}
                </div>
            </div>

            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6 text-gray-900">
                    <h3 class="text-lg font-semibold mb-4">Employee Directory</h3>
                    
                    <p class="mb-4">
                        Search and view employee information.
                    </p>

                    <a href="{{ route('employees.index') }}"
                       class="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                        Go to Employee Search
                    </a>
                </div>
            </div>

        </div>
    </div>
</x-app-layout>