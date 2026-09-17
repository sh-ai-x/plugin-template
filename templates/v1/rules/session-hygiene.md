# Session hygiene

- Treat plugin caches as disposable and read-only from hook code.
- Store durable project state in the consuming repository, not in the installed plugin.
- Keep secrets in environment variables or the host's secret store.
- Avoid `../` references and machine-specific absolute paths.
- Make update behavior explicit in the plugin README when a host caches or copies files.
