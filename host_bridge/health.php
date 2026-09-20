<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

$root = getenv('HOST_BRIDGE_ROOT') ?: '/home/zomorodm/zomorodmelal-app/django_project';
$tokenFile = getenv('HOST_BRIDGE_TOKEN_FILE') ?: '/home/zomorodm/.host_bridge_token';

echo json_encode([
    'ok' => is_dir($root),
    'service' => 'zomorodmelal-host-bridge',
    'https_required' => true,
    'root_exists' => is_dir($root),
    'token_configured' => is_readable($tokenFile) && trim((string)@file_get_contents($tokenFile)) !== '',
    'time' => gmdate('c')
], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
