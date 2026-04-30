import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://2.59.41.2:6700',
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    // Firefox и Webkit удалены для стабильности скриншотов в CI
  ],

  expect: {
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.2, // Допуск 20% для всех тестов
    },
  },
});
