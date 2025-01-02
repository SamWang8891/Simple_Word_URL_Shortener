<!DOCTYPE html>
<html lang="en">

<?php
session_start();
if (!isset($_SESSION['use'])) {
    echo "<script>alert('Please log in first!');</script>";
    header("Location: login.php");
    exit();
}

if (isset($_POST['login'])) {
    $old_user = $_POST['old_user'];
    $new_user = $_POST['new_user'];
    $new_pass = $_POST['new_pass'];

    $old_user = base64_encode($old_user);
    $new_user = base64_encode($new_user);
    $new_pass = base64_encode($new_pass);
    $old_user = escapeshellarg($old_user);
    $new_user = escapeshellarg($new_user);
    $new_pass = escapeshellarg($new_pass);


    if (shell_exec("echo $old_user $new_user $new_pass | python3 /app/python/change_cred.py") === '1') {
        echo "<script>alert('Credential changed successfully!');</script>";
        header("Location: login.php");
    } 
    else {
        echo "<script>alert('Old username is incorrect. Please try again.');</script>";
    }
}
?>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener</title>
    <link rel="icon" href="images/favicon.ico" type="image/x-icon">
    <style>
        body {
            image-rendering: pixelated;
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
    <h1>Change Credential</h1>
    <form method="post" action="">
        <label for="old_user">Old Username:</label>
        <input type="text" id="old_user" name="old_user" required>

        <label for="pass">New Username:</label>
        <input type="text" id="new_user" name="new_user" required>

        <label for="pass">New Password:</label>
        <input type="password" id="new_pass" name=" new_pass" required>

        <button type="submit" name="login">Login</button>
    </form>
</body>

</html>