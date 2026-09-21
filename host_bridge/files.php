<?php
declare(strict_types=1);

/**
 * Zomorod Melal authenticated host file API.
 *
 * Required:
 *   HOST_BRIDGE_TOKEN or HOST_BRIDGE_TOKEN_FILE
 * Optional:
 *   HOST_BRIDGE_ROOT (defaults to the cPanel application root)
 *   HOST_BRIDGE_AUDIT_FILE
 *
 * This endpoint intentionally provides file operations only.
 * It never executes arbitrary shell commands.
 */

const DEFAULT_ROOT = '/home/zomorodm/zomorodmelal-app';
const DEFAULT_TOKEN_FILE = '/home/zomorodm/.host_bridge_token';
const DEFAULT_AUDIT_FILE = '/home/zomorodm/.host_bridge_audit.log';
const MAX_BODY_BYTES = 4 * 1024 * 1024;

function respond(int $code, array $data): never {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}
function envv(string $key, ?string $default = null): ?string {
    $v = getenv($key);
    return ($v === false || $v === '') ? $default : $v;
}
function token(): string {
    $direct = envv('HOST_BRIDGE_TOKEN');
    if ($direct !== null) return trim($direct);
    $file = envv('HOST_BRIDGE_TOKEN_FILE', DEFAULT_TOKEN_FILE);
    return is_readable($file) ? trim((string)file_get_contents($file)) : '';
}
function auth(): void {
    $https = (($_SERVER['HTTPS'] ?? '') === 'on');
    $forwarded = strtolower(trim((string)($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '')));
    $trustedForwarded = ($_SERVER['REMOTE_ADDR'] ?? '') !== '' && (($_SERVER['REMOTE_ADDR'] ?? '') === ($_SERVER['SERVER_ADDR'] ?? ''));
    if (!$https && (!$trustedForwarded || $forwarded !== 'https')) {
        respond(400, ['ok'=>false, 'error'=>'https_required']);
    }
    $header = $_SERVER['HTTP_AUTHORIZATION'] ?? '';
    if ($header === '' && function_exists('getallheaders')) {
        foreach (getallheaders() as $k => $v) {
            if (strcasecmp($k, 'Authorization') === 0) { $header = (string)$v; break; }
        }
    }
    $provided = preg_match('/^Bearer\s+(.+)$/i', trim($header), $m) ? trim($m[1]) : '';
    $expected = token();
    if ($expected === '' || $provided === '' || !hash_equals($expected, $provided)) {
        respond(401, ['ok' => false, 'error' => 'unauthorized']);
    }
}
function root(): string {
    $r = realpath(envv('HOST_BRIDGE_ROOT', DEFAULT_ROOT));
    if ($r === false || !is_dir($r)) respond(500, ['ok'=>false,'error'=>'bridge_root_unavailable']);
    return rtrim($r, DIRECTORY_SEPARATOR);
}
function rel(string $p): string {
    $p = str_replace(["\\", "\0"], ["/", ""], trim($p));
    $p = ltrim($p, "/");
    if ($p === '' || $p === '.') return '';
    $parts = [];
    foreach (explode('/', $p) as $part) {
        if ($part === '' || $part === '.') continue;
        if ($part === '..') respond(400, ['ok'=>false,'error'=>'path_traversal_rejected']);
        $parts[] = $part;
    }
    return implode(DIRECTORY_SEPARATOR, $parts);
}
function inside(string $path, string $root): bool {
    return $path === $root || str_starts_with($path, $root . DIRECTORY_SEPARATOR);
}
function existing(string $root, string $relative): string {
    $candidate = $relative === '' ? $root : $root . DIRECTORY_SEPARATOR . $relative;
    $real = realpath($candidate);
    if ($real === false || !inside($real, $root)) respond(404, ['ok'=>false,'error'=>'path_not_found_or_outside_root']);
    return $real;
}
function parent_path(string $root, string $relative): string {
    $parentRel = dirname($relative);
    $parentRel = $parentRel === '.' ? '' : $parentRel;
    $parent = existing($root, $parentRel);
    if (!is_dir($parent)) respond(400, ['ok'=>false,'error'=>'parent_not_directory']);
    return $parent;
}
function audit(string $action, string $path, bool $ok): void {
    $file = envv('HOST_BRIDGE_AUDIT_FILE', DEFAULT_AUDIT_FILE);
    $row = json_encode([
        'time'=>gmdate('c'),
        'ip'=>$_SERVER['REMOTE_ADDR'] ?? 'unknown',
        'action'=>$action,
        'path'=>$path,
        'success'=>$ok
    ], JSON_UNESCAPED_SLASHES);
    @file_put_contents($file, $row.PHP_EOL, FILE_APPEND|LOCK_EX);
}
function body(): array {
    if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0) > MAX_BODY_BYTES) respond(413,['ok'=>false,'error'=>'request_too_large']);
    $raw = file_get_contents('php://input');
    $data = json_decode((string)$raw, true);
    if (!is_array($data)) respond(400,['ok'=>false,'error'=>'valid_json_body_required']);
    return $data;
}
function meta(string $path, string $root): array {
    return [
        'path'=>str_replace(DIRECTORY_SEPARATOR,'/',ltrim(str_replace($root,'',$path),DIRECTORY_SEPARATOR)),
        'type'=>is_dir($path)?'directory':'file',
        'size'=>is_file($path)?filesize($path):null,
        'modified'=>date('c',(int)filemtime($path)),
        'permissions'=>substr(sprintf('%o',fileperms($path)),-4)
    ];
}

auth();
if ($_SERVER['REQUEST_METHOD'] !== 'POST') respond(405,['ok'=>false,'error'=>'POST_required']);

$data = body();
$action = (string)($data['action'] ?? '');
$relative = rel((string)($data['path'] ?? ''));
$root = root();

try {
    switch ($action) {
        case 'status':
            respond(200,['ok'=>true,'service'=>'zomorodmelal-host-file-api','root'=>$root,'writable'=>is_writable($root),'timestamp'=>gmdate('c')]);

        case 'list_directory':
            $path = existing($root,$relative);
            if (!is_dir($path)) respond(400,['ok'=>false,'error'=>'not_a_directory']);
            $items=[];
            foreach (scandir($path) ?: [] as $name) {
                if ($name==='.' || $name==='..') continue;
                $child=realpath($path.DIRECTORY_SEPARATOR.$name);
                if ($child!==false && inside($child,$root)) $items[]=meta($child,$root);
            }
            audit($action,$relative,true);
            respond(200,['ok'=>true,'items'=>$items]);

        case 'read_file':
            $path=existing($root,$relative);
            if (!is_file($path) || !is_readable($path)) respond(400,['ok'=>false,'error'=>'file_not_readable']);
            $max=(int)envv('HOST_BRIDGE_MAX_READ_BYTES','2097152');
            $size=(int)filesize($path);
            if ($size>$max) respond(413,['ok'=>false,'error'=>'file_too_large','size'=>$size,'max'=>$max]);
            $content=file_get_contents($path);
            if ($content===false) respond(500,['ok'=>false,'error'=>'read_failed']);
            audit($action,$relative,true);
            respond(200,['ok'=>true,'path'=>$relative,'content'=>$content,'size'=>$size,'sha256'=>hash('sha256',$content)]);

        case 'write_file':
        case 'create_file':
            if ($relative==='') respond(400,['ok'=>false,'error'=>'file_path_required']);
            $content=$data['content'] ?? null;
            if (!is_string($content)) respond(400,['ok'=>false,'error'=>'content_string_required']);
            $max=(int)envv('HOST_BRIDGE_MAX_WRITE_BYTES','4194304');
            if (strlen($content)>$max) respond(413,['ok'=>false,'error'=>'content_too_large','max'=>$max]);
            $target=$root.DIRECTORY_SEPARATOR.$relative;
            $exists=file_exists($target);
            if ($action==='create_file' && $exists) respond(409,['ok'=>false,'error'=>'file_already_exists']);
            if ($exists) {
                if (is_link($target)) respond(400,['ok'=>false,'error'=>'symlink_target_rejected']);
                $target=realpath($target);
                if ($target===false || !inside($target,$root) || !is_file($target)) respond(400,['ok'=>false,'error'=>'existing_target_invalid']);
            } else {
                $parent=parent_path($root,$relative);
                $target=$parent.DIRECTORY_SEPARATOR.basename($relative);
            }
            if (file_put_contents($target,$content,LOCK_EX)===false) {
                audit($action,$relative,false); respond(500,['ok'=>false,'error'=>'write_failed']);
            }
            audit($action,$relative,true);
            respond(200,['ok'=>true,'path'=>$relative,'bytes'=>strlen($content),'sha256'=>hash('sha256',$content)]);

        case 'create_directory':
            if ($relative==='') respond(400,['ok'=>false,'error'=>'directory_path_required']);
            $target=$root.DIRECTORY_SEPARATOR.$relative;
            if (file_exists($target)) respond(409,['ok'=>false,'error'=>'path_already_exists']);
            $parent=parent_path($root,$relative);
            if (!mkdir($parent.DIRECTORY_SEPARATOR.basename($relative),0755,false)) {
                audit($action,$relative,false); respond(500,['ok'=>false,'error'=>'mkdir_failed']);
            }
            audit($action,$relative,true);
            respond(200,['ok'=>true,'path'=>$relative]);

        case 'delete_file':
            if ($relative==='') respond(400,['ok'=>false,'error'=>'cannot_delete_root']);
            $path=existing($root,$relative);
            if (!is_file($path)) respond(400,['ok'=>false,'error'=>'file_required']);
            if (!unlink($path)) {
                audit($action,$relative,false); respond(500,['ok'=>false,'error'=>'delete_failed']);
            }
            audit($action,$relative,true);
            respond(200,['ok'=>true,'path'=>$relative]);

        case 'file_info':
            $path=existing($root,$relative);
            audit($action,$relative,true);
            respond(200,['ok'=>true,'file'=>meta($path,$root)]);

        default:
            respond(400,['ok'=>false,'error'=>'unsupported_action','actions'=>['status','list_directory','read_file','write_file','create_file','create_directory','delete_file','file_info']]);
    }
} catch (Throwable $e) {
    audit($action,$relative,false);
    respond(500,['ok'=>false,'error'=>'bridge_internal_error']);
}
