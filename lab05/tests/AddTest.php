<?php
use PHPUnit\Framework\TestCase;
require_once __DIR__ . '/../php-app/index.php';

final class AddTest extends TestCase {
  public function testAdd(): void {
    $this->assertSame(5, add(2,3));
  }
}
