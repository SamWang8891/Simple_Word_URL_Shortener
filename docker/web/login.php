<!DOCTYPE html>
<html lang="en">

<?php
session_start();

$expireTime = 3600;
if (isset($_SESSION['LAST_ACTIVITY']) && (time() - $_SESSION['LAST_ACTIVITY'] > $expireTime)) {
    session_unset();  
    session_destroy();   
}
$_SESSION['LAST_ACTIVITY'] = time(); 

if (isset($_SESSION['use'])) {
    header("Location:admin.php");
    exit();
}

if (isset($_POST['login'])) {
    $user = $_POST['user'];
    $pass = $_POST['pass'];

    #$user = base64_encode($user);
    #$pass = base64_encode($pass);
    #$user = escapeshellarg($user);
    #$pass = escapeshellarg($pass);
    
    $input = "$user\\n$pass";

    $result = shell_exec("echo -e $input | python3 /docker/python/check_pass.py");
    echo $result;
    
    #echo "<script>alert('$result');</script>";

    if (shell_exec("echo -e '$result' | python3 /docker/python/check_pass.py") === '1') {
        $_SESSION['use'] = $user;
        header("Location:admin.php");
        exit();
    }
    else {
        echo "<script>alert('Username or password is incorrect. Please try again.');</script>";
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

        input[type="password"] {
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
    <h1>Admin Login</h1>

    <form method="post" action="">
        <label for="user">Username:</label>
        <input type="text" id="user" name="user" required>

        <label for="pass">Password:</label>
        <input type="password" id="pass" name="pass" required>
        <br>
        <button type="submit" name="login">Login</button>
    </form>
    
    <form method="get" action="change_cred.php">
        <button type="submit" class="purge-button">Change Credentials</button>
    </form>
    
</body>

</html>