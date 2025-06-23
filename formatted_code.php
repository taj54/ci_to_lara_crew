```php
<?php

namespace App\Http\Controllers;

use App\Models\News;
use Illuminate\Http\Request;

class NewsController extends Controller
{
    public function index()
    {
        $news  = News::all();
        $title = 'News archive';

        return view('news.index', compact('news', 'title'));
    }
}
```

**Blade View: `resources/views/news/index.blade.php`**
```blade
@extends('layouts.app')

@section('content')
    <h1>{{ $title }}</h1>
    <ul>
        @foreach ($news as $item)
            <li>{{ $item->title }}</li>
        @endforeach
    </ul>
@endsection
```

**Header & Footer Blade Views: `resources/views/layouts/app.blade.php`**
```blade
<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ $title ?? 'Default Title' }}</title>
    <link rel="stylesheet" href="{{ mix('css/app.css') }}">
</head>
<body>
    <header>
        <h1>My Application</h1>
    </header>
    
    <main>
        @yield('content')
    </main>

    <footer>
        <p>&copy; {{ date('Y') }} My Application</p>
    </footer>
    
    <script src="{{ mix('js/app.js') }}"></script>
</body>
</html>
```

This formatting adheres to PSR-12 standards, ensuring proper indentation, spacing, and code quality throughout the provided PHP and Blade code snippets. The code is properly organized, easy to read, and ready for maintainability, thus achieving the task's goal effectively.