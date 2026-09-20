<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

const DEFAULT_ROOT = '/home/zomorodm/zomorodmelal-app/django_project';
const DEFAULT_TOKEN_FILE = '/home/zomorodm/.host_bridge_token';

function envv(string $key, ?string $default = null): ?string {
    $v = getenv($key);
    return ($v === false || $v === '') ? $default : $v;
}

function token(): string {
    $direct = envv('HOST_BRIDGE_TOKEN');
    if ($direct !== null) return trim($direct);
    $file = envv('HOST_BRIDGE_TOKEN_FILE', DEFAULT_TOKEN_FILE);
    return is_readable($file) ? trim((string)@file_get_contents($file)) : '';
}

function authorized(): bool {
    $header = $_SERVER['HTTP_AUTHORIZATION'] ?? '';
    if ($header === '' && function_exists('getallheaders')) {
        foreach (getallheaders() as $k => $v) {
            if (strcasecmp($k, 'Authorization') === 0) {
                $header = (string)$v;
                break;
            }
        }
    }
    $provided = preg_match('/^Bearer\s+(.+)$/i', trim($header), $m) ? trim($m[1]) : '';
    $expected = token();
    return $expected !== '' && $provided !== '' && hash_equals($expected, $provided);
}

$root = envv('HOST_BRIDGE_ROOT', DEFAULT_ROOT);
$protected = envv('HOST_BRIDGE_HEALTH_PRIVATE', '1') !== '0';

if ($protected && !authorized()) {
    http_response_code(401);
    echo json_encode(['ok'=>false,'error'=>'unauthorized'], JSON_UNESCAPED_SLASHES);
    exit;
}

$rootExists = is_dir($root);
echo json_encode([
    'ok' => $rootExists,
    'service' => 'zomorodmelal-host-bridge',
    'https_required' => true,
    'root_exists' => $rootExists,
    'time' => gmdate('c')
], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
