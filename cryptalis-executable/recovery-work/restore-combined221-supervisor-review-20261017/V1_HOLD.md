# External recovery supervisor V1: HOLD

Seal d490c743243146310cb09a5d80d7047540e72ecfee548e0e13a630a0433acdd5.
Controller ac923baba59f053beabe5992a243085dc5a383db566e9aec948086dbc35909eb.
Helper ee0908cf7e1dec9287b9f2f448ae40186ba11fcc3ecfc69c2c40448564a89063.

Blocking owned-child signal gap: controller interrupted() raises KeyboardInterrupt for SIGINT/SIGTERM while bounded() performs proc = subprocess.Popen(...). An asynchronous exception after child creation and before the assignment can leave proc=None; the helper finally then cannot kill/reap that child. Blocking signals only upon entering finally is too late. The same raising handler can also interrupt the transition into signal blocking.

Retain this sealed version unexecuted. Narrow immutable successor should install record-only catchable-signal handlers, explicitly check cancellation before spawn and in the capture loop, and keep cleanup/afterchecks noninterrupting. No widening of archive, inputs, resources or restored source is needed. Do not treat this HOLD as source acceptance or execution clearance.

Other observed intended controls: 38 static plus four dynamic inputs, original mailbox pin included, exact one parser command, shell-free child, finite wall/stream and five child resource limits, waitid(WNOWAIT), kill before reap on failure, best-effort complete metadata-first afterchecks and explicit descendant-absence limitation. These observations do not override the blocker.

All sealed member hashes were checked as inert data. No controller/helper/parser import, execution, compilation, extraction or test was performed.
