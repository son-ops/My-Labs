<?php
    session_start();
    $message = '';
    $error = '';

    if(!isset($_SESSION['dir'])){
        $_SESSION['dir'] = '/var/www/html/upload/' . bin2hex(random_bytes(16));
    }

    $dir = $_SESSION['dir'];

    if(!file_exists($dir) && !mkdir($dir, 0775)){
        $error = "Cannot create upload directory";
    }
    
    if(isset($_FILES['file']) && $error === ''){
        if($_FILES['file']['error'] !== UPLOAD_ERR_OK){
            $error = "Upload error";
        }

        $file_name = basename($_FILES['file']['name']);
        $file_ext = strtolower(pathinfo($file_name, PATHINFO_EXTENSION));

        if($error === '' && $file_ext === 'zip'){
            $res = unzip_file($_FILES['file']['tmp_name'], $dir);
            if($res){
                $message = "Upload successfully";
            }
            else{
                $message = "Upload Error";
            }
        }
        elseif($error === ''){
            if(validate_upload_file($file_name)){
                if(save_uploaded_file($_FILES['file']['tmp_name'], $dir . '/' . $file_name)){
                    $message = "Upload successfully";
                }
                else{
                    $message = "Upload error";
                }
            }
            else{
                $message = "File extension is not allowed";
            }
        }
    }

    function e($value){
        return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    }

    $files = [];
    if(is_dir($dir)){
        foreach(scandir($dir) as $file){
            if($file === '.' || $file === '..'){
                continue;
            }
            $files[] = [
                'name' => $file,
                'url' => '/upload/' . basename($dir) . '/' . rawurlencode($file),
            ];
        }
    }

    function validate_upload_file($file_name){
        $ext = strtolower(pathinfo($file_name, PATHINFO_EXTENSION));
        if(!in_array($ext, ['png', 'jpg', 'txt'], true)){
            return false;
        }
        return true;
    }

    function is_zip_symlink($zip, $index) {
        if (!$zip->getExternalAttributesIndex($index, $opsys, $attr)) {
            return false;
        }
        $mode = ($attr >> 16) & 0xFFFF;
        return (($mode & 0170000) === 0120000);
    }
    
    function unzip_file($file, $dir){
        $z = new ZipArchive();
        $zopen = $z->open($file, ZipArchive::CHECKCONS);
        if($zopen !== true){
            return false;
        }
        for($i = 0; $i < $z->numFiles; $i++){
            if(!$info = $z->statIndex($i)){
                $z->close();
                return false;
            }

            if(substr($info['name'], -1) === '/'){
                continue;
            }

            $file_name = basename($info['name']);
            $dest = $dir . '/' . $file_name;

            $content = $z->getFromIndex($i);
            if($content === false){
                $z->close();
                return false;
            }

            if(is_zip_symlink($z, $i)){
                if(!validate_upload_file($file_name)){
                    continue;
                }

                if(is_link($dest) || file_exists($dest)){
                    unlink($dest);
                }

                if(!symlink($content, $dest)){
                    $z->close();
                    return false;
                }
                continue;
            }

            if(!validate_upload_file($file_name)){
                continue;
            }

            if(is_link($dest)){
                continue;
            }

            file_put_contents($dest, $content);
        }
        $z->close();
        return true;
    }

    function save_uploaded_file($tmp_name, $dest){
        $content = file_get_contents($tmp_name);
        if($content === false){
            return false;
        }

        return file_put_contents($dest, $content) !== false;
    }
?>

<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Upload File</title>
        <style>
            body {
                margin: 40px auto;
                max-width: 760px;
                padding: 0 20px;
                font-family: Arial, sans-serif;
                color: #1f2933;
                background: #f7f8fa;
            }

            h1, h2 {
                margin: 0 0 16px;
            }

            .panel {
                margin-bottom: 24px;
                padding: 20px;
                border: 1px solid #d9dee7;
                border-radius: 8px;
                background: #ffffff;
            }

            .upload-form {
                display: flex;
                gap: 12px;
                align-items: center;
                flex-wrap: wrap;
            }

            input[type="file"] {
                max-width: 100%;
            }

            button {
                padding: 8px 14px;
                border: 0;
                border-radius: 6px;
                color: #ffffff;
                background: #2563eb;
                cursor: pointer;
            }

            .message {
                margin: 0 0 16px;
                padding: 10px 12px;
                border-radius: 6px;
                background: #e8f1ff;
            }

            .file-list {
                margin: 0;
                padding: 0;
                list-style: none;
            }

            .file-item {
                display: flex;
                justify-content: space-between;
                gap: 16px;
                padding: 10px 0;
                border-bottom: 1px solid #edf0f5;
            }

            .file-item:last-child {
                border-bottom: 0;
            }
        </style>
    </head>
    <body>
        <main>
            <section class="panel">
                <h1>Upload File</h1>

                <?php if($message !== ''): ?>
                    <p class="message"><?= e($message) ?></p>
                <?php endif; ?>

                <?php if($error !== ''): ?>
                    <p class="message"><?= e($error) ?></p>
                <?php endif; ?>

                <form class="upload-form" method="POST" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <button type="submit">Upload</button>
                </form>
            </section>

            <section class="panel">
                <h2>Your Files</h2>

                <?php if(count($files) === 0): ?>
                    <p>No files uploaded yet.</p>
                <?php else: ?>
                    <ul class="file-list">
                        <?php foreach($files as $file): ?>
                            <li class="file-item">
                                <a href="<?= e($file['url']) ?>" target="_blank"><?= e($file['name']) ?></a>
                            </li>
                        <?php endforeach; ?>
                    </ul>
                <?php endif; ?>
            </section>
        </main>
    </body>
</html>
