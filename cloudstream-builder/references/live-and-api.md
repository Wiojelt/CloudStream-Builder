# Live channels and authorized app APIs

Use live/API mode only for sources the user has placed in scope. Inspect the current API or web request flow without exporting account credentials, private cookies, or device identifiers.

## Channel contract

Each channel needs a stable display name, category, logo when available, and a playback payload that can be resolved at play time. Do not publish one generic card containing a whole playlist unless the user explicitly requests a grouped provider.

Preserve all working backup streams and label them. Avoid hard-coding short-lived media URLs when a stable resolver request is available. If domains rotate, discover them from the provider's own redirect/config mechanism and validate the final host before use.

## API inspection

Record the minimum reproducible request shape: method, endpoint role, non-secret headers, request fields, response model, and token lifetime. Implement public or permitted application logic, not device-bound credentials. Keep encrypted/obfuscated endpoint details in source only when they are necessary for function and the user has authorized that source; never expose them in README logs.

## Categories and logos

Use the source's category labels, then normalize only duplicates and whitespace. Resolve lazy/relative logos and provide a provider-level fallback. If every country is included, expose a country/category selection mechanism rather than flooding the home page.

## Verification

Test at least one channel per distinct resolver shape, not necessarily every channel. A playlist entry is not verified until its current resolver returns playable media and CloudStream accepts the link type and headers.
