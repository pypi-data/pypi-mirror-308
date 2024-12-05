prepositions = (
    "aboard",
    "about",
    "above",
    "across",
    "after",
    "the",
    "against",
    "along",
    "amid",
    "among",
    "around",
    "as",
    "at",
    "before",
    "behind",
    "below",
    "beneath",
    "beside",
    "between",
    "beyond",
    "but",
    "by",
    "concerning",
    "considering",
    "despite",
    "down",
    "during",
    "except",
    "following",
    "for",
    "from",
    "in",
    "inside",
    "into",
    "like",
    "minus",
    "near",
    "next",
    "of",
    "off",
    "on",
    "onto",
    "opposite",
    "out",
    "outside",
    "over",
    "past",
    "per",
    "plus",
    "regarding",
    "round",
    "save",
    "since",
    "than",
    "through",
    "till",
    "to",
    "toward",
    "under",
    "underneath",
    "unlike",
    "until",
    "up",
    "upon",
    "versus",
    "via",
    "with",
    "within",
    "without",
)

stop_words = (
    '"',
    "-",
    "'ll",
    "'ve",
    "&",
    "#",
    "^",
    "000",
    "0o",
    "0s",
    "3a",
    "3b",
    "3d",
    "6b",
    "6o",
    "a's",
    "a",
    "A",
    "a1",
    "a2",
    "a3",
    "a4",
    "ab",
    "able",
    "about",
    "above",
    "abst",
    "ac",
    "acc",
    "accordance",
    "according",
    "accordingly",
    "across",
    "act",
    "actually",
    "ad",
    "added",
    "adj",
    "ae",
    "af",
    "affected",
    "affecting",
    "affects",
    "after",
    "afterwards",
    "ag",
    "again",
    "against",
    "ah",
    "ain't",
    "ain",
    "airport",
    "aj",
    "al",
    "all",
    "allow",
    "allows",
    "almost",
    "alone",
    "along",
    "already",
    "also",
    "although",
    "always",
    "am",
    "among",
    "amongst",
    "amoungst",
    "amount",
    "an",
    "and",
    "announce",
    "another",
    "any",
    "anybody",
    "anyhow",
    "anymore",
    "anyone",
    "anything",
    "anyway",
    "anyways",
    "anywhere",
    "ao",
    "ap",
    "apart",
    "apparently",
    "appear",
    "appreciate",
    "appropriate",
    "approximately",
    "ar",
    "archived",
    "are",
    "area",
    "areas",
    "aren't",
    "aren",
    "arent",
    "arise",
    "around",
    "as",
    "aside",
    "ask",
    "asking",
    "associated",
    "at",
    "au",
    "auth",
    "av",
    "available",
    "aw",
    "away",
    "awfully",
    "ax",
    "ay",
    "az",
    "b",
    "B",
    "b1",
    "b2",
    "b3",
    "ba",
    "back",
    "bad",
    "based",
    "bc",
    "bd",
    "be",
    "became",
    "because",
    "become",
    "becomes",
    "becoming",
    "been",
    "before",
    "beforehand",
    "begin",
    "beginning",
    "beginnings",
    "begins",
    "behind",
    "being",
    "believe",
    "below",
    "beside",
    "besides",
    "best",
    "better",
    "between",
    "beyond",
    "bi",
    "bill",
    "billion",
    "biol",
    "bj",
    "bk",
    "bl",
    "bn",
    "boring",
    "both",
    "bottom",
    "bp",
    "br",
    "brief",
    "briefly",
    "bs",
    "bt",
    "bu",
    "built",
    "bus",
    "buses",
    "but",
    "bx",
    "by",
    "c",
    "C",
    "c1",
    "c2",
    "c3",
    "ca",
    "call",
    "called",
    "came",
    "can't",
    "can",
    "cannot",
    "cant",
    "cause",
    "causes",
    "cc",
    "cd",
    "ce",
    "century",
    "certain",
    "certainly",
    "cf",
    "cg",
    "ch",
    "changes",
    "ci",
    "cit",
    "cities",
    "city",
    "civilian",
    "cj",
    "cl",
    "clearly",
    "cm",
    "cn",
    "co",
    "com",
    "come",
    "comes",
    "con",
    "concerning",
    "confused",
    "consequently",
    "consider",
    "considering",
    "contain",
    "containing",
    "contains",
    "corresponding",
    "could",
    "couldn't",
    "couldn",
    "couldnt",
    "country",
    "course",
    "cp",
    "cq",
    "cr",
    "cry",
    "cs",
    "ct",
    "cu",
    "currently",
    "cv",
    "cx",
    "cy",
    "cz",
    "d",
    "D",
    "d2",
    "da",
    "daily",
    "date",
    "day",
    "days",
    "dc",
    "dd",
    "de",
    "definitely",
    "describe",
    "described",
    "description",
    "despite",
    "detail",
    "df",
    "di",
    "did",
    "didn't",
    "didn",
    "different",
    "district",
    "dj",
    "dk",
    "dl",
    "do",
    "does",
    "doesn't",
    "doesn",
    "doing",
    "don't",
    "don",
    "done",
    "down",
    "downwards",
    "dp",
    "dr",
    "ds",
    "dt",
    "du",
    "due",
    "during",
    "dx",
    "dy",
    "e",
    "E",
    "e2",
    "e3",
    "ea",
    "each",
    "east",
    "ec",
    "ed",
    "edu",
    "ee",
    "ef",
    "effect",
    "eg",
    "ei",
    "eight",
    "eighty",
    "either",
    "ej",
    "el",
    "eleven",
    "else",
    "elsewhere",
    "em",
    "empty",
    "en",
    "end",
    "ending",
    "english",
    "enough",
    "entire",
    "entirely",
    "eo",
    "ep",
    "eq",
    "er",
    "es",
    "especially",
    "est",
    "et",
    "etc",
    "eu",
    "ev",
    "even",
    "events",
    "ever",
    "every",
    "everybody",
    "everyone",
    "everything",
    "everywhere",
    "ex",
    "exactly",
    "example",
    "except",
    "ey",
    "f",
    "F",
    "f2",
    "fa",
    "far",
    "fc",
    "few",
    "ff",
    "fi",
    "fifteen",
    "fifth",
    "fifty",
    "fify",
    "fill",
    "find",
    "fire",
    "first",
    "five",
    "fix",
    "fj",
    "fl",
    "flights",
    "fn",
    "fo",
    "follow",
    "followed",
    "following",
    "follows",
    "for",
    "former",
    "formerly",
    "forth",
    "forty",
    "found",
    "four",
    "fr",
    "from",
    "front",
    "fs",
    "ft",
    "fu",
    "full",
    "further",
    "furthermore",
    "fy",
    "g",
    "G",
    "ga",
    "gave",
    "ge",
    "generally",
    "get",
    "gets",
    "getting",
    "gi",
    "give",
    "given",
    "gives",
    "giving",
    "gj",
    "gl",
    "go",
    "goes",
    "going",
    "gone",
    "good",
    "got",
    "gotten",
    "government",
    "gr",
    "greetings",
    "gs",
    "gy",
    "h",
    "H",
    "h2",
    "h3",
    "had",
    "hadn't",
    "hadn",
    "happens",
    "hardly",
    "has",
    "hasn't",
    "hasn",
    "hasnt",
    "have",
    "haven't",
    "haven",
    "having",
    "he'd",
    "he'll",
    "he's",
    "he",
    "hed",
    "held",
    "hello",
    "help",
    "hence",
    "her",
    "here's",
    "here",
    "hereafter",
    "hereby",
    "herein",
    "heres",
    "hereupon",
    "hers",
    "herself",
    "hes",
    "hh",
    "hi",
    "hid",
    "him",
    "himself",
    "his",
    "hither",
    "hj",
    "ho",
    "home",
    "hopefully",
    "hour",
    "hours",
    "how's",
    "how",
    "howbeit",
    "however",
    "hr",
    "hs",
    "http",
    "hu",
    "hundred",
    "hy",
    "i'd",
    "i'll",
    "i'm",
    "i've",
    "i",
    "I",
    "i2",
    "i3",
    "i4",
    "i6",
    "i7",
    "i8",
    "ia",
    "ib",
    "ibid",
    "ic",
    "id",
    "ie",
    "if",
    "ig",
    "ignored",
    "ih",
    "ii",
    "ij",
    "il",
    "im",
    "immediate",
    "immediately",
    "importance",
    "important",
    "in",
    "inasmuch",
    "inc",
    "include",
    "including",
    "indeed",
    "index",
    "indicate",
    "indicated",
    "indicates",
    "information",
    "inner",
    "insofar",
    "instead",
    "interest",
    "interesting",
    "into",
    "invention",
    "inward",
    "io",
    "ip",
    "iq",
    "ir",
    "is",
    "isn't",
    "isn",
    "it'd",
    "it'll",
    "it's",
    "it’s",
    "it",
    "itd",
    "its",
    "itself",
    "iv",
    "ix",
    "iy",
    "iz",
    "j",
    "J",
    "japanese",
    "jj",
    "jr",
    "js",
    "jt",
    "ju",
    "just",
    "k",
    "K",
    "ke",
    "keep",
    "keeps",
    "kept",
    "kg",
    "killed",
    "kj",
    "km",
    "know",
    "known",
    "knows",
    "ko",
    "l",
    "L",
    "l2",
    "la",
    "large",
    "largely",
    "largest",
    "last",
    "lately",
    "later",
    "latter",
    "latterly",
    "lb",
    "lc",
    "le",
    "least",
    "left",
    "les",
    "less",
    "lest",
    "let's",
    "let",
    "lets",
    "lf",
    "life",
    "like",
    "liked",
    "likely",
    "line",
    "list",
    "little",
    "lj",
    "ll",
    "ln",
    "lo",
    "local",
    "located",
    "long",
    "look",
    "looking",
    "looks",
    "los",
    "lr",
    "ls",
    "lt",
    "ltd",
    "m",
    "M",
    "m2",
    "ma",
    "made",
    "main",
    "mainly",
    "major",
    "make",
    "makes",
    "many",
    "map",
    "match",
    "may",
    "maybe",
    "me",
    "mean",
    "means",
    "meantime",
    "meanwhile",
    "medium",
    "merely",
    "mg",
    "mi",
    "mi)",
    "might",
    "mightn't",
    "mightn",
    "mill",
    "million",
    "million)",
    "mine",
    "miss",
    "ml",
    "mn",
    "mo",
    "month",
    "more",
    "moreover",
    "most",
    "mostly",
    "move",
    "mr",
    "mrs",
    "ms",
    "mt",
    "mu",
    "much",
    "mug",
    "must",
    "mustn't",
    "mustn",
    "my",
    "myself",
    "n",
    "N",
    "n2",
    "na",
    "name",
    "namely",
    "national",
    "nay",
    "nc",
    "nd",
    "ne",
    "near",
    "nearest",
    "nearly",
    "necessarily",
    "necessary",
    "need",
    "needn't",
    "needn",
    "needs",
    "neither",
    "never",
    "nevertheless",
    "new",
    "next",
    "ng",
    "ni",
    "night",
    "nine",
    "ninety",
    "nj",
    "nl",
    "nn",
    "no",
    "nobody",
    "non",
    "none",
    "nonetheless",
    "noone",
    "nor",
    "normally",
    "north",
    "nos",
    "not",
    "noted",
    "nothing",
    "novel",
    "now",
    "nowhere",
    "nr",
    "ns",
    "nt",
    "number",
    "numerous",
    "ny",
    "o",
    "O",
    "oa",
    "ob",
    "obtain",
    "obtained",
    "obviously",
    "oc",
    "od",
    "of",
    "off",
    "often",
    "og",
    "oh",
    "oi",
    "oj",
    "ok",
    "okay",
    "ol",
    "old",
    "om",
    "omitted",
    "on",
    "once",
    "one",
    "ones",
    "only",
    "onto",
    "oo",
    "op",
    "oq",
    "or",
    "ord",
    "original",
    "os",
    "ot",
    "other",
    "others",
    "otherwise",
    "ou",
    "ought",
    "our",
    "ours",
    "ourselves",
    "out",
    "outside",
    "over",
    "overall",
    "ow",
    "owing",
    "own",
    "ox",
    "oz",
    "p",
    "P",
    "p1",
    "p2",
    "p3",
    "page",
    "pagecount",
    "pages",
    "par",
    "part",
    "participated",
    "particular",
    "particularly",
    "pas",
    "past",
    "pc",
    "pd",
    "pe",
    "per",
    "perhaps",
    "pf",
    "ph",
    "photo",
    "photo#",
    "pi",
    "picture",
    "pj",
    "pk",
    "pl",
    "place",
    "placed",
    "played",
    "please",
    "plus",
    "pm",
    "pn",
    "po",
    "political",
    "poorly",
    "popular",
    "population",
    "possible",
    "possibly",
    "potentially",
    "pp",
    "pq",
    "pr",
    "predominantly",
    "present",
    "presumably",
    "previously",
    "primarily",
    "private",
    "probably",
    "promptly",
    "proud",
    "provides",
    "province",
    "provincial",
    "ps",
    "pt",
    "pu",
    "put",
    "py",
    "q",
    "Q",
    "qj",
    "qu",
    "que",
    "quickly",
    "quite",
    "qv",
    "r",
    "R",
    "r2",
    "ra",
    "ran",
    "rather",
    "rc",
    "rd",
    "re",
    "readily",
    "really",
    "reasonably",
    "received",
    "recent",
    "recently",
    "ref",
    "refs",
    "regarding",
    "regardless",
    "regards",
    "region",
    "related",
    "relatively",
    "research",
    "respectively",
    "resulted",
    "resulting",
    "results",
    "rf",
    "rh",
    "ri",
    "right",
    "rj",
    "rl",
    "rm",
    "rn",
    "ro",
    "road",
    "role",
    "route",
    "rq",
    "rr",
    "rs",
    "rt",
    "ru",
    "run",
    "runs",
    "rv",
    "ry",
    "s",
    "S",
    "s2",
    "sa",
    "said",
    "same",
    "saw",
    "say",
    "saying",
    "says",
    "sc",
    "sd",
    "se",
    "season",
    "sec",
    "second",
    "secondly",
    "section",
    "see",
    "seeing",
    "seem",
    "seemed",
    "seeming",
    "seems",
    "seen",
    "self",
    "selves",
    "sensible",
    "sent",
    "series",
    "serious",
    "seriously",
    "service",
    "services",
    "seven",
    "several",
    "sf",
    "shall",
    "shan't",
    "shan",
    "she'd",
    "she'll",
    "she's",
    "she",
    "shed",
    "shes",
    "should've",
    "should",
    "shouldn't",
    "shouldn",
    "show",
    "showed",
    "shown",
    "showns",
    "shows",
    "si",
    "side",
    "significant",
    "significantly",
    "similar",
    "similarly",
    "since",
    "sincere",
    "six",
    "sixty",
    "sj",
    "sl",
    "slightly",
    "sm",
    "small",
    "sn",
    "so",
    "some",
    "somebody",
    "somehow",
    "someone",
    "somethan",
    "something",
    "sometime",
    "sometimes",
    "somewhat",
    "somewhere",
    "soon",
    "sorry",
    "south",
    "sp",
    "specifically",
    "specified",
    "specify",
    "specifying",
    "sq",
    "sr",
    "ss",
    "st",
    "standard",
    "started",
    "state",
    "station",
    "still",
    "stop",
    "strongly",
    "sub",
    "substantially",
    "successfully",
    "such",
    "sufficiently",
    "suggest",
    "sup",
    "sure",
    "sy",
    "system",
    "sz",
    "t's",
    "t",
    "T",
    "t1",
    "t2",
    "t3",
    "take",
    "taken",
    "takes",
    "taking",
    "taxi",
    "tb",
    "tc",
    "td",
    "te",
    "team",
    "tell",
    "ten",
    "tends",
    "terrible",
    "tf",
    "th",
    "than",
    "thank",
    "thanks",
    "thanx",
    "that'll",
    "that's",
    "that've",
    "that",
    "thats",
    "the",
    "their",
    "theirs",
    "them",
    "themselves",
    "then",
    "thence",
    "there'll",
    "there's",
    "there've",
    "there",
    "thereafter",
    "thereby",
    "thered",
    "therefore",
    "therein",
    "thereof",
    "therere",
    "theres",
    "thereto",
    "thereupon",
    "these",
    "they'd",
    "they'll",
    "they're",
    "they've",
    "they",
    "theyd",
    "theyre",
    "thick",
    "thickv",
    "thin",
    "think",
    "third",
    "this",
    "thorough",
    "thoroughly",
    "those",
    "thou",
    "though",
    "thoughh",
    "thousand",
    "three",
    "throug",
    "through",
    "throughout",
    "thru",
    "thus",
    "ti",
    "til",
    "time",
    "times",
    "tip",
    "tj",
    "tl",
    "tm",
    "tn",
    "to",
    "together",
    "too",
    "took",
    "top",
    "total",
    "toward",
    "towards",
    "tp",
    "tq",
    "tr",
    "train",
    "travel",
    "tried",
    "tries",
    "truly",
    "try",
    "trying",
    "ts",
    "tt",
    "tv",
    "twelve",
    "twenty",
    "twice",
    "two",
    "tx",
    "u",
    "U",
    "u201d",
    "ue",
    "ui",
    "uj",
    "uk",
    "um",
    "un",
    "under",
    "unfortunately",
    "unless",
    "unlike",
    "unlikely",
    "until",
    "unto",
    "uo",
    "up",
    "upon",
    "uprising",
    "ups",
    "ur",
    "us",
    "use",
    "used",
    "useful",
    "usefully",
    "usefulness",
    "uses",
    "using",
    "usually",
    "ut",
    "v",
    "V",
    "va",
    "value",
    "various",
    "vd",
    "ve",
    "very",
    "via",
    "viz",
    "vj",
    "vo",
    "vol",
    "vols",
    "volumtype",
    "vq",
    "vs",
    "vt",
    "vu",
    "w",
    "W",
    "wa",
    "want",
    "wants",
    "was",
    "wasn't",
    "wasn",
    "wasnt",
    "way",
    "we'd",
    "we'll",
    "we're",
    "we've",
    "we",
    "wed",
    "welcome",
    "well-b",
    "well",
    "went",
    "were",
    "weren't",
    "weren",
    "werent",
    "west",
    "what'll",
    "what's",
    "what",
    "whatever",
    "whats",
    "when's",
    "when",
    "whence",
    "whenever",
    "where's",
    "where",
    "whereafter",
    "whereas",
    "whereby",
    "wherein",
    "wheres",
    "whereupon",
    "wherever",
    "whether",
    "which",
    "while",
    "whim",
    "whither",
    "who'll",
    "who's",
    "who",
    "whod",
    "whoever",
    "whole",
    "whom",
    "whomever",
    "whos",
    "whose",
    "why's",
    "why",
    "wi",
    "widely",
    "will",
    "willing",
    "wish",
    "with",
    "within",
    "without",
    "wo",
    "won't",
    "won",
    "wonder",
    "wont",
    "words",
    "world",
    "would",
    "wouldn't",
    "wouldn",
    "wouldnt",
    "www",
    "x",
    "X",
    "x1",
    "x2",
    "x3",
    "xf",
    "xi",
    "xj",
    "xk",
    "xl",
    "xn",
    "xo",
    "xs",
    "xt",
    "xv",
    "xx",
    "y",
    "Y",
    "y2",
    "year",
    "years",
    "yes",
    "yet",
    "yj",
    "yl",
    "you'd",
    "you'll",
    "you're",
    "you've",
    "you",
    "youd",
    "your",
    "youre",
    "yours",
    "yourself",
    "yourselves",
    "yr",
    "ys",
    "yt",
    "z",
    "Z",
    "zero",
    "zi",
    "zz",
)
