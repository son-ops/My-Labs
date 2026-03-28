<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Search</title>
</head>
<body>
    <h1>Employee Search</h1>

    <form method="POST" action="{{ route('employees.search') }}">
        @csrf

        <div>
            <label for="keyword">Keyword</label>
            <input
                type="text"
                id="keyword"
                name="keyword"
                value="{{ old('keyword') }}"
                placeholder="Search by name or email"
            >
        </div>

        <br>

        <div>
            <label for="department">Department</label>
            <select id="department" name="department">
                <option value="">All</option>
                <option value="IT" {{ old('department') == 'IT' ? 'selected' : '' }}>IT</option>
                <option value="HR" {{ old('department') == 'HR' ? 'selected' : '' }}>HR</option>
                <option value="Finance" {{ old('department') == 'Finance' ? 'selected' : '' }}>Finance</option>
                <option value="Marketing" {{ old('department') == 'Marketing' ? 'selected' : '' }}>Marketing</option>
                <option value="Sales" {{ old('department') == 'Sales' ? 'selected' : '' }}>Sales</option>
            </select>
        </div>

        <br>

        <div>
            <label for="country">Country</label>
            <select id="country" name="country">
                <option value="">All</option>
                <option value="Vietnam" {{ old('country') == 'Vietnam' ? 'selected' : '' }}>Vietnam</option>
                <option value="Japan" {{ old('country') == 'Japan' ? 'selected' : '' }}>Japan</option>
                <option value="Singapore" {{ old('country') == 'Singapore' ? 'selected' : '' }}>Singapore</option>
                <option value="Thailand" {{ old('country') == 'Thailand' ? 'selected' : '' }}>Thailand</option>
                <option value="USA" {{ old('country') == 'USA' ? 'selected' : '' }}>USA</option>
            </select>
        </div>

        <br>

        <div>
            <label for="view_mode">View Mode</label>
            <select id="view_mode" name="view_mode">
                <option value="basic" {{ old('view_mode') == 'basic' ? 'selected' : '' }}>Basic</option>
                <option value="hr" {{ old('view_mode') == 'hr' ? 'selected' : '' }}>HR</option>
                <option value="manager" {{ old('view_mode') == 'manager' ? 'selected' : '' }}>Manager</option>
            </select>
        </div>

        <br>

        <div>
            <label for="sort_mode">Sort Mode</label>
            <select id="sort_mode" name="sort_mode">
                <option value="name_asc" {{ old('sort_mode') == 'name_asc' ? 'selected' : '' }}>Name ASC</option>
                <option value="name_desc" {{ old('sort_mode') == 'name_desc' ? 'selected' : '' }}>Name DESC</option>
                <option value="department_asc" {{ old('sort_mode') == 'department_asc' ? 'selected' : '' }}>Department ASC</option>
                <option value="newest" {{ old('sort_mode') == 'newest' ? 'selected' : '' }}>Newest</option>
                <option value="oldest" {{ old('sort_mode') == 'oldest' ? 'selected' : '' }}>Oldest</option>
            </select>
        </div>

        <br>

        <button type="submit">Search</button>
    </form>

    @if ($errors->any())
        <hr>
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    @endif

    @isset($rows)
        <hr>
        <h2>Search Results</h2>

        <table border="1" cellpadding="8" cellspacing="0">
            <thead>
                <tr>
                    <th>Full Name</th>
                    <th>Email</th>
                    <th>Department</th>
                    <th>Country</th>
                    <th>Salary Band</th>
                    <th>Created At</th>
                </tr>
            </thead>
            <tbody>
                @forelse ($rows as $row)
                    <tr>
                        <td>{{ $row->full_name ?? '' }}</td>
                        <td>{{ $row->email ?? '' }}</td>
                        <td>{{ $row->department ?? '' }}</td>
                        <td>{{ $row->country ?? '' }}</td>
                        <td>{{ $row->salary_band ?? '' }}</td>
                        <td>{{ $row->created_at ?? '' }}</td>
                    </tr>
                @empty
                    <tr>
                        <td colspan="6">No employees found.</td>
                    </tr>
                @endforelse
            </tbody>
        </table>
    @endisset
</body>
</html>