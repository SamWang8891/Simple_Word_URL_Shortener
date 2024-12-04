<!DOCTYPE html>
<html lang="en">

<?php
// Redirect Section
$request_url = $_SERVER['REQUEST_URI'];

if ($request_url === '/' || $request_url === '/index.php') {
    // Do nothing
} else {
    $request_url = ltrim($request_url, '/');
    $output = shell_exec("echo $request_url | python3 /app/python/search_record.py");
    header("Location: $output");
    exit();
}
?>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener</title>
    <link rel="icon" href="images/favicon.ico" type="image/x-icon">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8f5;
            color: #333;
            margin: 20px;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }

        h1 {
            color: #32cd32;
        }

        form {
            background-color: #fff;
            border: 2px solid #32cd32;
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            width: 90%;
            max-width: 400px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }

        input[type="text"] {
            width: calc(100% - 22px);
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }

        button {
            background-color: #32cd32;
            color: #fff;
            border: none;
            border-radius: 4px;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 16px;
        }

        button:hover {
            background-color: #28a428;
        }

        .purge-button {
            background-color: #ff0000;
        }

        .purge-button:hover {
            background-color: #cc0000;
        }

        p {
            background-color: #e0f7e0;
            border: 1px solid #32cd32;
            border-radius: 4px;
            padding: 10px;
            width: 90%;
            max-width: 400px;
            text-align: center;
            margin: 10px 0;
        }
    </style>
</head>

<body>
    <h1>URL Shortener</h1>
    <form method="post">
        <label for="create_url">Enter URL to shorten:</label>
        <input type="text" id="create_url" name="create_url">
        <button type="submit" name="action" value="create">Shorten URL</button>
    </form>
    <br>
    <form method="post">
        <label for="delete_url">Enter URL to delete (any should do):</label>
        <input type="text" id="delete_url" name="delete_url">
        <button type="submit" name="action" value="delete">Delete URL</button>
    </form>
    <br>
    <form method="post">
        <div style="display: flex; justify-content: space-between;">
            <button type="button" class="return-home" onclick="window.location.href='/'">Go Home</button>
            <button type="submit" name="action" value="purge" class="purge-button">Purge All URLs</button>
        </div>
    </form>

    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $action = $_POST['action'];

        if ($action === 'create' && !empty($_POST['create_url'])) {
            $create_url = escapeshellarg($_POST['create_url']);
            $output = shell_exec("echo $create_url | python3 /app/python/create_record.py");
            echo "<p>Shortened URL: <a href=\"$output\" target=\"_blank\">$output</a></p>";
        } elseif ($action === 'delete' && !empty($_POST['delete_url'])) {
            $delete_url = escapeshellarg($_POST['delete_url']);
            $output = shell_exec("echo $delete_url | python3 /app/python/delete_record.py");
            echo "<p>$output</p>";
        } elseif ($action === 'purge') {
            $output = shell_exec("python3 /app/python/delete_every_record.py");
            echo "<p>$output</p>";
        }
    }
    ?>
</body>

</html>
