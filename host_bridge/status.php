<?php
declare(strict_types=1);

/**
 * Zomorod Melal Host Bridge - read-only status endpoint.
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');

$readToken = getenv('GIT_BRIDGE_READ_TOKEN') ?: '';

if ($readToken !== '') {
    $auth = $_SERVER['HTTP_AUTHORIZATION'] ?? '';
    if (!preg_match('/^Bearer\\s+(.+)$/i', $auth, $m) || !hash_equals($readToken, trim($m[1]))) {
        http_response_code(401);
        echo json_encode(['ok' => false, 'error' => 'Unauthorized'], JSON_UNESCAPED_UNICODE);
        exit;
    }
}

if (isset($_GET['health'])) {
    echo json_encode([
        'ok' => true,
        'service' => 'zomorodmelal-host-bridge',
        'mode' => 'read-only',
        'time' => gmdate('c')
    ], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit;
}

$file = dirname(__DIR__) . '/../.zomorod_bridge/git-status.json';

if (!is_file($file)) {
    echo json_encode([
        'ok' => true,
        'status' => 'no_report',
        'message' => 'No deployment report has been received yet.'
    ], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit;
}

$data = json_decode((string)file_get_contents($file), true);

if (!is_array($data)) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'Invalid stored report'], JSON_UNESCAPED_UNICODE);
    exit;
}

echo json_encode([
    'ok' => true,
    'bridge' => 'zomorodmelal-host-bridge',
    'read_only' => true,
    'report' => $data
], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
