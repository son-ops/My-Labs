<?php
    session_start();
    if(!isset($_SESSION['dir'])){
        $_SESSION['dir'] = '/var/www/html/uploads/' . bin2hex(random_bytes(16));
    }
    $dir = $_SESSION['dir'];
    if( !file_exists($dir)){
        mkdir($dir);
    }
    if(isset($_FILES['file'])){
        try {
            $ext = strtolower(pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION));
            if($ext === 'zip'){
                $res = unzip_file($_FILES['file']['tmp_name'], $dir);
                if($res){
                    $message = "Upload zip file successfully";
                }
                else{
                    $error = "Upload zip file failed";
                }
            }
            else {
                $new_file = $dir . '/' . bin2hex(random_bytes(16)) . ($ext ? '.' . $ext : '');
                if(move_uploaded_file($_FILES['file']['tmp_name'], $new_file)){
                    $message = "Upload file successfully";
                }
                else{
                    $error = "Upload file failed";
                }
            }
        }
        catch(Exception $e) {
            $error = $e->getMessage();
        }
    }

    function unzip_file($file, $dir){
        $z = new ZipArchive();
        $zopen = $z->open($file, ZipArchive::CHECKCONS);
        if($zopen !== true){
            return false;
        }
        for($i=0; $i < $z->numFiles; $i++){
            if(! $info = $z->statIndex($i)){
                return false;
            }
            if( '/' === substr($info['name'],-1) || '/' === $info['name'][0]){
                continue;
            }
            $content = $z->getFromIndex($i);
            if($content === false){
                return false;
            }
            $name = str_replace('../', '', $info['name']);
            if(file_exists($dir)){
                $to_file = $dir . '/' . $name;
                file_put_contents($to_file, $content);
            }
        }
        $z->close();
        return true;
    }
    if (is_dir($dir)) {
        $items = scandir($dir);
        foreach ($items as $item) {
            if ($item === '.' || $item === '..') {
                continue;
            }
    
            $full_path = $dir . '/' . $item;
            if (is_file($full_path)) {
                $uploaded_files[] = [
                    'name' => $item,
                    'size' => filesize($full_path),
                    'mtime' => filemtime($full_path),
                ];
            }
        }
    }
?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload File</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <h1>Upload File</h1>

        <?php if (!empty($message)): ?>
            <div class="success">
                <?= htmlspecialchars($message, ENT_QUOTES, 'UTF-8') ?>
            </div>
        <?php endif; ?>

        <?php if (!empty($error)): ?>
            <div class="error">
                <?= htmlspecialchars($error, ENT_QUOTES, 'UTF-8') ?>
            </div>
        <?php endif; ?>

        <form enctype="multipart/form-data" method="POST">
            <input type="file" name="file" required>
            <input type="submit" value="Upload">
        </form>

        <div class="note">
            Hỗ trợ upload file thường hoặc file ZIP.
        </div>

        <br><h3>Danh sách file đã upload</h3>

        <?php if (!empty($uploaded_files)): ?>
            <div class="file-list">
                <?php foreach ($uploaded_files as $file): ?>
                    <a href="<?= str_replace('/var/www/html/','',$dir) ?>/<?= $file['name']?>">
                    <div class="file-item">
                        <div class="file-name">
                            <?= htmlspecialchars($file['name'], ENT_QUOTES, 'UTF-8') ?>
                        </div>
                        </a>    
                        <div class="file-meta">
                            Size: <?= (int)$file['size'] ?> bytes<br>
                            Modified: <?= date('Y-m-d H:i:s', $file['mtime']) ?>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        <?php else: ?>
            <p class="empty">Chưa có file nào trong thư mục upload hiện tại.</p>
        <?php endif; ?>

    </div>
</body>
</html>
