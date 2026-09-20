<?php
declare(strict_types=1);

/**
 * Zomorod Melal Host Bridge - write endpoint.
 *
 * Accepts a small JSON deployment report from GitHub Actions.
 * No shell execution, no Git commands, no arbitrary commands.
 */

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'POST required'], JSON_UNESCAPED_UNICODE);
    exit;
}

$secret = getenv('GIT_BRIDGE_WEBHOOK_SECRET') ?: '';
$provided = $_SERVER['HTTP_X_BRIDGE_TOKEN'] ?? '';

if ($secret === '' || $provided === '' || !hash_equals($secret, $provided)) {
    http_response_code(401);
    echo json_encode(['ok' => false, 'error' => 'Unauthorized'], JSON_UNESCAPED_UNICODE);
    exit;
}

$raw = file_get_contents('php://input');
if ($raw === false || strlen($raw) > 262144) {
    http_response_code(413);
    echo json_encode(['ok' => false, 'error' => 'Invalid payload size'], JSON_UNESCAPED_UNICODE);
    exit;
}

$data = json_decode($raw, true);
if (!is_array($data)) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'JSON required'], JSON_UNESCAPED_UNICODE);
    exit;
}

$allowed = [
    'status', 'repository', 'branch', 'commit', 'workflow',
    'run_id', 'run_number', 'job', 'message', 'error',
    'timestamp', 'environment'
];

$out = [];
foreach ($allowed as $key) {
    if (array_key_exists($key, $data) && is_scalar($data[$key])) {
        $out[$key] = substr((string)$data[$key], 0, 4000);
    }
}

$out['received_at'] = gmdate('c');

$base = dirname(__DIR__) . '/../.zomorod_bridge';
if (!is_dir($base) && !mkdir($base, 0700, true)) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'Storage unavailable'], JSON_UNESCAPED_UNICODE);
    exit;
}

$file = $base . '/git-status.json';
$json = json_encode($out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);

if ($json === false || file_put_contents($file, $json, LOCK_EX) === false) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'Write failed'], JSON_UNESCAPED_UNICODE);
    exit;
}

@chmod($file, 0600);

echo json_encode(['ok' => true, 'received_at' => $out['received_at']], JSON_UNESCAPED_UNICODE);
