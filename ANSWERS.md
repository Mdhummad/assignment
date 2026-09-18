# Log reading assignment

1. **Start:** The first affected request was at **2026-07-02 14:32:40.073**; its worker failed at **14:32:42.692**. The logs do not pinpoint the exact instant the underlying fault began. The preceding deployment was logged at **14:31:13.000**.
2. **Endpoint:** `POST /checkout`. The first request returned HTTP `202` with `request_id=16ce72300cf58a32`, but the matching worker entry says `upstream call failed ... err=ECONNRESET ... (retries exhausted)`. All **2,385** worker failures correlate to this endpoint; the HTTP `202` only confirms acceptance of asynchronous work.
3. **Pattern:** All **2,385** failed checkout jobs have **odd `user_id`** values and occur after the start above. After that point, **2,385 of 2,741** odd-user checkout jobs failed (87.0%), versus **0 of 2,886** even-user jobs. Another **356** odd-user jobs completed, so odd IDs are a strong pattern, not a sufficient condition. Before the incident, **2,102** odd-user and **2,146** even-user checkout jobs completed.
4. **Distinct affected users:** **2,335**, counting unique `user_id` values for failed checkout jobs.

**Possible cause:** Release `v2.14.3` (commit `219c39f`) was deployed at **14:31:13.000**, shortly before the first failure. Every worker failure reports `ECONNRESET` from `10.0.3.44:8443` after retries. This points to a broken upstream connection or routing path associated with the deployment, but the logs alone cannot prove which change caused it.

## Investigation process

- Read the web and worker logs and correlated entries using `request_id`.
- Checked the first failed worker job against its original web request.
- Counted failures by endpoint, response status, and user ID parity.
- Compared checkout jobs before and after the first failure.
- Counted distinct affected user IDs.
- Checked deployment entries and upstream error details.
- Set aside recurring `metrics-worker` analytics upload timeouts: they predate the checkout failures and are not correlated with checkout request IDs.
