# 🦀 Rust-Projects: 100 Handcrafted Rust Implementations

A structured, comprehensive collection of **100 complete, standalone Rust projects** spanning systems programming, concurrency, data structures, compilers, networking, and algorithms.

Organized progressively from **Simple** to **Intermediate** and **Advanced**.

---

## 📊 Repository Structure Overview

| Level | Projects | Count | Focus Areas |
| :--- | :--- | :---: | :--- |
| 🟢 **Simple** | `001` - `035` | 35 | Language basics, CLI tools, string manipulation, traits, standard collections |
| 🟡 **Intermediate** | `036` - `070` | 35 | Concurrency, thread pools, HTTP/DNS protocols, caching, trees, compression |
| 🔴 **Advanced** | `071` - `100` | 30 | Bytecode VMs, actor systems, Raft consensus, vector search, lock-free queues, JIT |
| **Total** | `001` - `100` | **100** | Full spectrum of idiomatic Rust programming |

---

## 🚀 Running Any Project

Each project is a standalone Cargo package using pure Rust (`std`).

```bash
# Navigate to any project directory
cd 001_number_guessing_game

# Run the program
cargo run

# Run built-in test suite
cargo test
```

---

## 🛠️ Automated Commit & Push Script

This repository includes a shell script [`commit_and_push.sh`](./commit_and_push.sh) designed to commit each project individually across directories to create a clear, granular git history.

### Usage:

```bash
# 1. Preview changes (Dry run)
./commit_and_push.sh --dry-run

# 2. Commit all projects locally directory by directory
./commit_and_push.sh --commit-only

# 3. Commit and push directory by directory to remote
./commit_and_push.sh --push

# 4. Resume from a specific project number (e.g. 42)
./commit_and_push.sh --from 42 --push
```

---

## 📚 Complete Project Index

### 🟢 Level 1: Simple & Fundamental Projects (001 - 035)

| # | Project | Category | Description |
|---|---------|----------|-------------|
| `001` | [Number Guessing Game](./001_number_guessing_game) | `CLI & Game Logic` | Interactive number guessing game with binary search hint system, input validation, and attempts tracking. |
| `002` | [Temperature Converter](./002_temperature_converter) | `Math & Enums` | Multi-scale temperature converter supporting Celsius, Fahrenheit, and Kelvin with custom enum traits and precision rounding. |
| `003` | [Word Frequency Counter](./003_word_frequency_counter) | `Text & Collections` | Tokenizes text, strips punctuation, normalizes case, and counts word occurrences using HashMap and sorting. |
| `004` | [CLI Calculator](./004_cli_calculator) | `Parsing & Math` | Arithmetic calculator supporting +, -, *, /, parenthesis, and operator precedence using the Shunting-Yard algorithm. |
| `005` | [To-Do List CLI Manager](./005_todo_cli) | `Data Management & CRUD` | In-memory task organizer with priority levels, status transitions, formatted listing, and filtering. |
| `006` | [Palindrome Checker](./006_palindrome_checker) | `Strings & Algorithms` | Unicode and whitespace-agnostic palindrome validator with bidirectional iterator comparison. |
| `007` | [Fibonacci Generator](./007_fibonacci_generator) | `Math & Iterators` | Generates Fibonacci sequences via iterative, memoized, recursive, and custom infinite `Iterator` trait approaches. |
| `008` | [Prime Sieve & Factorizer](./008_prime_sieve) | `Algorithms & Math` | Sieve of Eratosthenes prime generator and prime factorization engine with performance metrics. |
| `009` | [Caesar Cipher Tool](./009_caesar_cipher) | `Cryptography & Strings` | Symmetric shift cipher encryptor and decryptor supporting arbitrary positive and negative key shifts. |
| `010` | [2D Matrix Operations](./010_matrix_operations) | `Linear Algebra` | Matrix data structure with addition, subtraction, scalar scaling, transposition, and dot-product multiplication. |
| `011` | [Physical Unit Converter](./011_unit_converter) | `Physics & Traits` | Trait-based physical dimension unit converter for distance, mass, and volume conversions. |
| `012` | [File Metadata Inspector](./012_file_metadata_inspector) | `Filesystem & I/O` | Inspects file size, permissions, file extension, and human-readable formatting of byte metrics. |
| `013` | [Configurable Password Generator](./013_password_generator) | `Security & Strings` | Generates secure randomized passwords with configurable entropy, character set inclusions, and strength ratings. |
| `014` | [Generic Stack & Queue](./014_stack_and_queue) | `Data Structures` | Generic implementations of LIFO Stack and FIFO Queue with peak, size, capacity, and iterator capabilities. |
| `015` | [Roman Numeral Converter](./015_roman_numeral_converter) | `Math & Strings` | Bi-directional converter between standard integers (1-3999) and Roman numerals with subtractive notation. |
| `016` | [Minimal JSON Field Extractor](./016_json_field_extractor) | `Parsing & Text` | Zero-dependency lightweight JSON string lexer and key-value extractor for flat objects. |
| `017` | [Robust CSV Table Parser](./017_csv_parser) | `File Formats & Parsing` | Parses CSV text adhering to RFC 4180 rules, correctly managing embedded commas, escape quotes, and line breaks. |
| `018` | [Luhn Algorithm Credit Card Validator](./018_luhn_algorithm) | `Algorithms & Validation` | Calculates and verifies checksum digits according to the Luhn (Mod 10) formula used in payment cards. |
| `019` | [Rock-Paper-Scissors Simulator](./019_rock_paper_scissors) | `Games & Enums` | Rock, Paper, Scissors, Lizard, Spock game logic with round scoring and strategy evaluation. |
| `020` | [Binary Search Tree](./020_binary_search_tree) | `Trees & Algorithms` | Recursive Binary Search Tree with node insertion, contains lookup, depth measurement, and in-order traversal. |
| `021` | [Run-Length Encoding (RLE)](./021_run_length_encoding) | `Compression & Strings` | Lossless data compression algorithm encoding repeated consecutive values into (count, char) tokens. |
| `022` | [Classic Sorting Suite](./022_sorting_algorithms) | `Algorithms` | Collection of standard sorting algorithms: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, and Quick Sort. |
| `023` | [Vector Statistical Calculator](./023_vector_statistics) | `Math & Statistics` | Calculates descriptive statistics: mean, median, mode, sample variance, standard deviation, and range. |
| `024` | [Morse Code Translator](./024_morse_code_translator) | `Strings & Encodings` | Bi-directional translator between text and International Morse Code with word-delimiter slash formatting. |
| `025` | [ANSI Terminal Styler](./025_ansi_color_formatter) | `CLI & Terminal` | ANSI escape code wrapper providing colorful bold, underlined, and foreground/background styled terminal text. |
| `026` | [Base64 Encoder & Decoder](./026_base64_encoder) | `Encodings & Cryptography` | Standard RFC 4648 Base64 byte-stream encoder and decoder with padding calculation. |
| `027` | [Dotenv (.env) File Parser](./027_env_var_loader) | `Parsing & Config` | Custom environment file reader parsing key-value pairs, ignoring comments, and stripping quotes. |
| `028` | [Precision Stopwatch & Lap Timer](./028_stopwatch_timer) | `Time & Benchmarking` | High-precision timer supporting start, pause, resume, and split lap timing using std::time::Instant. |
| `029` | [CRC-32 Checksum Digest](./029_hash_digest_crc32) | `Hashing & Cryptography` | Standard IEEE 802.3 CRC-32 checksum calculator with precomputed lookup table acceleration. |
| `030` | [Levenshtein Distance & Fuzzy Matcher](./030_levenshtein_distance) | `Dynamic Programming & NLP` | Calculates minimum single-character edit distance (insertions, deletions, substitutions) between strings. |
| `031` | [URL Query String Parser & Encoder](./031_url_query_parser) | `Web & Networking` | Parses and serializes URL query parameters with percent-encoding and decoding. |
| `032` | [Probabilistic Bloom Filter](./032_bloom_filter_simple) | `Probabilistic Data Structures` | Space-efficient probabilistic filter testing set membership with zero false negatives and tunable false positives. |
| `033` | [URL Slug Generator & Sanitizer](./033_slug_generator) | `Strings & Web` | Transforms arbitrary article headlines and product names into URL-friendly kebab-case slugs. |
| `034` | [Exact Rational Fraction Arithmetic](./034_fraction_arithmetic) | `Math & Operator Overloading` | Exact rational number implementation supporting +, -, *, / operator overloading with greatest common divisor (GCD) reduction. |
| `035` | [CLI Animated Progress Bar](./035_cli_progress_bar) | `CLI & Animation` | Terminal progress bar with percentage counter, spinner glyphs, and carriage return `\r` line rewriting. |

---

### 🟡 Level 2: Intermediate Projects (036 - 070)

| # | Project | Category | Description |
|---|---------|----------|-------------|
| `036` | [Reusable Worker Thread Pool](./036_thread_pool) | `Concurrency & Systems` | Multi-threaded worker pool dispatching closures across OS threads using synchronized mpsc channels. |
| `037` | [Persistent Key-Value Store](./037_kv_store_persisted) | `Databases & Storage` | Bitcask-inspired append-only log structured key-value store with in-memory HashMap offset index. |
| `038` | [LRU Cache (Least Recently Used)](./038_lru_cache) | `Data Structures & Caching` | O(1) capacity-bounded Least Recently Used cache implemented with a HashMap and index-linked doubly list. |
| `039` | [RFC 7230 HTTP/1.1 Parser](./039_http_parser) | `Networking & Protocols` | Zero-copy HTTP request and response parser parsing methods, status lines, headers, and body payloads. |
| `040` | [Abstract Syntax Tree (AST) Evaluator](./040_expression_evaluator) | `Compilers & Interpreters` | Recursive descent math expression parser producing an Abstract Syntax Tree (AST) with variable environments. |
| `041` | [Token Bucket Rate Limiter](./041_token_bucket_rate_limiter) | `Networking & Distributed Systems` | High-throughput token bucket rate limiter providing burst capacity and constant replenishment. |
| `042` | [Type-Safe Event Dispatcher](./042_event_emitter) | `Design Patterns` | Decoupled observer event bus registering callbacks and dispatching typed payload notifications. |
| `043` | [Huffman Coding & Compression](./043_huffman_coding) | `Algorithms & Compression` | Prefix-free variable-length binary encoding with Huffman tree generation, prefix tables, and lossless decode. |
| `044` | [Dijkstra's Shortest Path Algorithm](./044_dijkstra_pathfinding) | `Graphs & Algorithms` | Weighted graph shortest-path engine with BinaryHeap min-priority queue and path backtracking. |
| `045` | [Thompson's NFA Regex Engine](./045_mini_regex_engine) | `Compilers & Automata` | Non-deterministic Finite Automaton (NFA) regex engine supporting characters, wildcard `.`, and `*` repetition. |
| `046` | [Bump Arena Memory Allocator](./046_custom_arena_allocator) | `Memory & Systems` | Arena memory allocator providing contiguous linear buffer allocations with instant batch deallocation. |
| `047` | [Circular FIFO Ring Buffer](./047_circular_ring_buffer) | `Data Structures & Audio/IO` | Fixed-capacity circular queue with wrapping read/write pointers and overwriting or non-overwriting modes. |
| `048` | [Markdown to HTML Transpiler](./048_markdown_to_html) | `Compilers & Text` | Parses common Markdown syntax: headings (#), bold (**), italics (*), code blocks, and links into valid HTML. |
| `049` | [Concurrent TCP Echo Server](./049_tcp_echo_server) | `Networking & I/O` | Multi-threaded TCP network server accepting concurrent client streams and echoing back payload bytes. |
| `050` | [Myers Line Diff Engine](./050_diff_tool) | `Algorithms & Text` | Line-by-line file difference generator calculating added, deleted, and identical lines using Myers diff. |
| `051` | [Cron Expression Parser](./051_cron_expression_parser) | `Time & Scheduling` | 5-field cron parser supporting wildcards, exact values, lists, and intervals for minute/hour/dom/month/dow scheduling. |
| `052` | [Consistent Hashing Ring](./052_consistent_hashing) | `Distributed Systems` | Consistent hash ring with virtual nodes distributing keys evenly across dynamically joining/leaving server nodes. |
| `053` | [Trie (Prefix Tree) Autocomplete](./053_trie_prefix_tree) | `Data Structures & Strings` | Trie prefix tree supporting word insertion, exact word search, prefix lookup, and auto-complete word suggestions. |
| `054` | [Concurrent Stream Pipeline](./054_concurrency_pipeline) | `Concurrency & Channels` | Multi-stage stream processing pipeline communicating across concurrent stages using bounded mpsc channels. |
| `055` | [JWT (JSON Web Token) Structure Validator](./055_jwt_validator) | `Web & Security` | Parses and unpacks JWT tokens into Header, Payload, and Signature segments with Base64Url decoding. |
| `056` | [Circuit Breaker State Machine](./056_circuit_breaker) | `Distributed Systems` | Resilience pattern state machine (Closed, Open, HalfOpen) tripping on fault thresholds and recovering after timeout. |
| `057` | [RFC 4122 UUID v4 Generator](./057_uuid_v4_generator) | `Cryptography & IDs` | Standard 128-bit Universally Unique Identifier v4 generator setting version (4) and variant (RFC 4122) bits. |
| `058` | [Scalable Partitioned Bloom Filter](./058_bloom_filter_scalable) | `Probabilistic Data Structures` | Multi-slice Bloom filter dynamically growing additional layers as capacity fills to maintain bounded error rate. |
| `059` | [Generic Binary Min-Heap](./059_min_heap_priority_queue) | `Data Structures & Trees` | Binary min-heap with sift-up and sift-down algorithms implementing O(log n) push/pop and O(n) heapify. |
| `060` | [Cryptographic Binary Merkle Tree](./060_binary_merkle_tree) | `Cryptography & Blockchain` | Binary Merkle Tree generating root hashes and audit inclusion proofs for tamper-evident data verification. |
| `061` | [Type-State Workflow State Machine](./061_state_machine_workflow) | `Design Patterns & Types` | Compile-time verified finite state machine preventing invalid transitions using Rust's zero-cost typestate pattern. |
| `062` | [Reactive Observer Event Bus](./062_observer_pattern_bus) | `Design Patterns` | Topic-based pub/sub notification message bus with subscribe tokens and unsubscribe unregistration. |
| `063` | [Probabilistic Skip List](./063_skiplist) | `Data Structures & Search` | Multi-level probabilistic skip list achieving expected O(log n) search, insertion, and ordered traversal. |
| `064` | [POSIX UStar Tar Archive Reader](./064_tar_archive_reader) | `File Formats & Systems` | Parses standard 512-byte POSIX UStar tar headers extracting filename, size, octal permissions, and content. |
| `065` | [Binary DNS Packet Parser](./065_dns_packet_parser) | `Networking & Protocols` | Decodes binary RFC 1035 DNS wire packets including 12-byte header flags, query questions, and resource records. |
| `066` | [Semantic Versioning (SemVer 2.0.0) Parser](./066_semver_parser) | `Parsing & Comparison` | Full SemVer 2.0.0 parser with Major, Minor, Patch, pre-release tags, build metadata, and ordering precedence. |
| `067` | [CLI Argument Parser from Scratch](./067_command_line_arg_parser) | `CLI & Parsing` | Zero-dependency CLI argument parser supporting boolean flags (-v), key-value options (--port=8080), and positional args. |
| `068` | [Twitter Snowflake Distributed ID Generator](./068_distributed_id_snowflake) | `Distributed Systems` | 64-bit distributed chronological ID generator incorporating epoch timestamp, worker ID, datacenter ID, and sequence counter. |
| `069` | [Endian & Varint Binary Codec](./069_byte_buffer_reader_writer) | `Serialization & Binary` | Binary buffer reader/writer supporting Little-Endian, Big-Endian primitives, and Google Protocol Buffer Varint encoding. |
| `070` | [Augmented Interval Tree](./070_interval_tree) | `Trees & Computational Geometry` | Augmented Binary Search Tree storing numeric intervals with subtree max-endpoint caching for O(log n) overlap searches. |

---

### 🔴 Level 3: Advanced Projects (071 - 100)

| # | Project | Category | Description |
|---|---------|----------|-------------|
| `071` | [Stack-Based Bytecode Virtual Machine](./071_bytecode_virtual_machine) | `Virtual Machines & Compilers` | Full stack VM with instruction pointer, call frames, arithmetic, comparison, jumps, and bytecode execution loop. |
| `072` | [Mini Actor Model Concurrency System](./072_mini_actor_system) | `Concurrency & Distributed Systems` | Erlang/Akka-inspired Actor system with isolated actor mailboxes, asynchronous message passing, and state encapsulation. |
| `073` | [Raft Consensus Core State Machine](./073_raft_consensus_core) | `Distributed Systems & Consensus` | Core Raft protocol state machine modeling Follower, Candidate, and Leader roles, terms, voting, and heartbeats. |
| `074` | [Lock-Free SPSC Circular Queue](./074_lock_free_spsc_queue) | `Concurrency & Lock-Free` | Single-Producer Single-Consumer lock-free ring buffer using atomic operations with acquire-release memory orderings. |
| `075` | [Mini Git Content-Addressable Object Store](./075_mini_git_object_store) | `Version Control & Storage` | Content-addressable storage implementation mimicking Git: blob, tree, and commit objects addressed by cryptographic hashes. |
| `076` | [Vector Similarity Search Engine](./076_vector_similarity_search) | `AI & Vector Databases` | High-dimensional embedding index calculating Cosine Similarity and Euclidean distance for k-Nearest Neighbors (KNN). |
| `077` | [Custom Cooperative Async Executor](./077_custom_async_executor) | `Async & Systems` | Toy cooperative task scheduler simulating Rust's Future polling, Ready/Pending states, and task wakeups. |
| `078` | [B+ Tree Database Index](./078_b_tree_database_index) | `Databases & Trees` | Multi-way balanced B+ Tree search index with node splitting, key search, and range traversal. |
| `079` | [Log-Structured Merge Tree (LSM)](./079_lsm_tree_storage) | `Databases & Storage` | LSM-Tree storage architecture with in-memory MemTable (BTreeMap), write-ahead log (WAL), and SSTable compaction. |
| `080` | [Compiler Lexer, Parser & AST Builder](./080_compiler_lexer_parser) | `Compilers & Languages` | Lexical scanner and recursive descent parser transforming code strings into an Abstract Syntax Tree (AST). |
| `081` | [WebAssembly Binary Disassembler](./081_wasm_runtime_disassembler) | `Virtual Machines & Binary` | WebAssembly (.wasm) binary reader validating magic number, version, section IDs, and decoding opcode streams. |
| `082` | [Multi-Layer Perceptron (MLP) Neural Net](./082_neural_network_mlp) | `AI & Machine Learning` | 2-layer neural network with forward pass activation (Sigmoid) and error backpropagation training for XOR logic. |
| `083` | [Atomic Lock-Free Treiber Stack](./083_lock_free_stack_treiber) | `Concurrency & Lock-Free` | Lock-free concurrent Treiber stack utilizing atomic compare-and-swap (CAS) pointer updates. |
| `084` | [Inverted Index Full-Text Search Engine](./084_inverted_index_search_engine) | `Search & Information Retrieval` | Full-text search engine with term-document inverted posting lists, boolean AND/OR queries, and TF-IDF scoring. |
| `085` | [Shared Memory IPC Ring Buffer](./085_memory_mapped_ring_buffer) | `Systems & IPC` | Simulated shared-memory circular queue for inter-process communication (IPC) with atomic synchronization. |
| `086` | [High-Performance TLV Binary Codec](./086_binary_protocol_codec) | `Protocols & Networking` | Type-Length-Value (TLV) framing codec with packet magic, checksum calculation, and binary payload decoding. |
| `087` | [Single-Decree Paxos Consensus Simulator](./087_paxos_consensus_simulator) | `Distributed Systems & Consensus` | Simulation of classical single-decree Paxos: Prepare/Promise phase (Phase 1) and Propose/Accept phase (Phase 2). |
| `088` | [Tracing Mark-and-Sweep Garbage Collector](./088_garbage_collector_mark_sweep) | `Memory Management & Compilers` | Simulation of managed heap memory with root references, mark phase graph traversal, and sweep deallocation. |
| `089` | [SIMD Vectorized Linear Algebra](./089_simd_vector_math) | `High Performance & SIMD` | High-throughput 4-lane SIMD vector operations (dot product, cross product, normalization) with fallback scalar paths. |
| `090` | [QUIC Variable-Length Integer & Packet Framing](./090_quic_packet_framing) | `Networking & Protocols` | RFC 9000 QUIC variable-length integer encoding (1, 2, 4, 8 bytes) and Initial packet header framing. |
| `091` | [Multidimensional Spatial K-d Tree](./091_spatial_kdtree) | `Computational Geometry & Trees` | 2D/3D K-d tree space-partitioning data structure for fast nearest-neighbor search and range queries. |
| `092` | [Distributed Two-Phase Commit (2PC)](./092_distributed_two_phase_commit) | `Distributed Systems & Transactions` | Two-Phase Commit transaction coordinator and cohort participants supporting Prepare, Vote, Commit, and Abort rollback. |
| `093` | [Columnar Table Storage & RLE](./093_columnar_storage_format) | `Databases & Analytics` | Column-oriented table representation (Apache Parquet style) with vectorized projections and run-length encoding. |
| `094` | [Disjoint-Set (Union-Find) with Path Compression](./094_disjoint_set_union_find) | `Algorithms & Graphs` | Disjoint-Set Union (DSU) data structure with path compression and union by rank for Kruskal's Minimum Spanning Tree. |
| `095` | [Graph Convolutional Network (GCN) Layer](./095_graph_neural_net_conv) | `AI & Graph Neural Networks` | Graph Convolutional Network layer aggregating neighbor node features via normalized adjacency matrix multiplication. |
| `096` | [TLS 1.3 ClientHello Record Parser](./096_tls_record_protocol_parser) | `Cryptography & Security` | Wire decoder for TLS 1.3 records, handshake frames, ClientHello random bytes, session ID, and cipher suites. |
| `097` | [Sliding Window Percentile Metrics](./097_sliding_window_metrics) | `Observability & Metrics` | High-throughput sliding time window recording latencies and computing p50, p90, and p99 quantiles. |
| `098` | [Chandy-Lamport Distributed Snapshot](./098_chandy_lamport_snapshot) | `Distributed Systems` | Chandy-Lamport algorithm capturing a consistent global state across concurrent communicating processes without stopping the system. |
| `099` | [Toy JIT Machine Code Assembler](./099_jit_assembler_toy) | `Low-Level & JIT Compilers` | Encodes x86_64 machine opcodes (mov, add, ret) dynamically into executable memory format representation. |
| `100` | [Distributed Gossip-Protocol Cluster](./100_distributed_key_value_cluster) | `Distributed Systems` | Decentralized cluster communicating state via gossip anti-entropy protocol with heartbeat health detection. |

---

## ⚙️ Environment & Requirements

* **Rust:** Stable (edition 2021+)
* **Cargo:** Standard toolchain
* **OS:** Linux / macOS / Windows
* **Dependencies:** Self-contained standard library (`std`) implementations for immediate zero-download builds.

---

## 👤 Author

**Ramrup Satpati** (`RSNPIIT`)  
Indian Institute of Technology Madras (IIT Madras)

---

## 📄 License

GNU General Public License v3.0  
See [`LICENSE`](./LICENSE) for full terms.
