# Fast Streaming Aggregator Pattern (CineStream Architecture)

## Problem with Traditional Aggregators
Traditional catalog aggregators query multiple providers sequentially or buffer all results in a synchronized list and call `allJobs.joinAll()` before emitting any links to CloudStream. If even one provider is blocked, dead, or slow (taking 15–30s to time out), the entire CloudStream player UI hangs on a loading spinner, and users receive zero links until the slowest provider finishes.

## CineStream High-Speed Streaming Solution
The CineStream pattern solves this by transforming link collection from a "batch wait" model into an **immediate real-time stream**:

### 1. SupervisorScope & Concurrency Control
Isolate each provider's execution so one provider's HTTP failure or exception never cancels concurrent tasks:
```kotlin
supervisorScope {
    val concurrency = 16 // 8 on low-memory TV boxes
    val semaphore = Semaphore(concurrency)
```

### 2. Per-Provider Timeout (Crucial)
Wrap each provider search and link resolution in an independent timeout (e.g. 8.5 seconds). Dead domains or Cloudflare challenges are cancelled cleanly without holding concurrency slots:
```kotlin
semaphore.withPermit {
    withTimeoutOrNull(8500L) {
        try {
            scrapeProvider(provider, payload, onLinkFound)
        } catch (e: CancellationException) {
            if (!isActive) throw e
        } catch (e: Throwable) {
            // Ignore isolated provider failure
        }
    }
}
```

### 3. Immediate Link Emission with Concurrent Deduplication
Instead of buffering links in a list, emit each link **immediately** to the CloudStream player callback as soon as the extractor finds it:
```kotlin
val seenUrls = ConcurrentHashMap.newKeySet<String>()
val emitLink: (String, ExtractorLink) -> Unit = { providerName, rawLink ->
    val dedupeKey = "${rawLink.url}|${rawLink.headers}"
    if (seenUrls.add(dedupeKey)) {
        callback(wrapLink(providerName, rawLink))
    }
}
```
The CloudStream UI updates in real-time, allowing the user to start playback within 1–2 seconds.

### 4. Search Query Pruning
Do not loop through multiple search permutations blindly. Query the localized primary title first; if a result with high confidence (e.g. score >= 75) is matched, skip subsequent queries immediately. Only execute secondary queries (such as originalTitle or cleaned title) when the primary query returns no matching candidates.

### 5. Settings Change & Process Restart Dialog
When catalog provider settings or domains are modified, avoid in-place state corruption. Prompt the user to restart CloudStream immediately upon closing the settings dialog:
```kotlin
AlertDialog.Builder(context)
    .setTitle("CloudStream")
    .setMessage("Ayarları değiştirdiniz, CloudStream'i yeniden başlatmanız lazım.")
    .setPositiveButton("Tamam") { _, _ ->
        android.os.Process.killProcess(android.os.Process.myPid())
        kotlin.system.exitProcess(0)
    }
    .setCancelable(false)
    .show()
```
