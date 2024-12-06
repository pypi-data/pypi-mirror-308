import logging
import warnings
from collections import defaultdict

from nxlu.config import Intent, PathIntent
from nxlu.constants import PathConcepts
from nxlu.explanation.entities import EntityExtractor

warnings.filterwarnings("ignore")

logger = logging.getLogger("nxlu")

__all__ = [
    "PathQueryAnalyzer",
    "filter_path_algorithms",
]


class PathQueryAnalyzer:
    """Enhanced analyzer incorporating intent classification and comprehensive path
    semantics.
    """

    def __init__(self):
        self.concepts = PathConcepts()
        self.entity_extractor = EntityExtractor()

    def analyze_query(
        self, query: str, intents: list[Intent]
    ) -> tuple[bool, bool, set[PathIntent]]:
        """
        Analyze query for path-related semantics and intents.

        Parameters
        ----------
        query : str
            The query to analyze
        intents : List[Intent]
            List of classified general intents for the query

        Returns
        -------
        Tuple[bool, bool, Set[PathIntent]]
            Has source, has target, and set of identified path intents
        """
        if not query:
            return False, False, set()

        # normalize query
        query_lower = query.lower()

        # identify path intents from general intents
        path_intents = set()
        for intent in intents:
            mapped_intent = self.concepts.GENERAL_TO_PATH_INTENT.get(intent)
            if mapped_intent:
                path_intents.add(mapped_intent)

        # identify additional path intents based on indicator words
        for path_intent, indicators in self.concepts.INTENT_INDICATORS.items():
            if any(indicator in query_lower for indicator in indicators):
                path_intents.add(path_intent)

        # detect entities with indicators
        sources = self.entity_extractor.extract_entities(
            query, self.concepts.SOURCE_INDICATORS
        )
        targets = self.entity_extractor.extract_entities(
            query, self.concepts.TARGET_INDICATORS
        )

        # initial flags based on detected indicators
        has_source = bool(sources)
        has_target = bool(targets)

        # handle cases where only target is found
        if not has_source and has_target:
            # treat the target as the source
            has_source = True
            has_target = False
            sources = targets  # reassign targets to sources
            targets = []

        # handle cases where no source/target indicators are found
        if not has_source and not has_target:
            entities = self.entity_extractor.extract_all_entities(query)
            if entities:
                if len(entities) == 1:
                    # single entity without indicators, treat as source
                    has_source = True
                    sources = entities
                elif len(entities) > 1:
                    # multiple entities, assign first as source, second as target
                    has_source = True
                    has_target = True
                    sources = [entities[0]]
                    targets = [entities[1]]

        # infer source/target presence from certain path intents if not already detected
        if (
            PathIntent.CAUSAL_PATH in path_intents
            or PathIntent.DIAGNOSTIC_PATH in path_intents
        ) and not (has_source and has_target):
            has_source = True
            has_target = True

        return has_source, has_target, path_intents


def filter_path_algorithms(
    algorithms: list[str],
    query: str | None = None,
    intents: list[Intent] | None = None,
) -> list[str]:
    """Filter algorithms based on query semantics and intent classification.

    Parameters
    ----------
    algorithms : List[str]
        List of algorithm names to filter
    query : Optional[str]
        The user's query
    intents : Optional[List[Intent]]
        List of classified intents for the query

    Returns
    -------
    List[str]
        Filtered list of algorithm names
    """
    if query is None:
        return algorithms

    analyzer = PathQueryAnalyzer()
    has_source, has_target, path_intents = analyzer.analyze_query(
        query, intents or [Intent.EXPLORATION]
    )

    filtered_algorithms = []
    exclusion_reasons = defaultdict(set)

    for algo in algorithms:
        # only apply filtering to path algorithms
        if algo in PathConcepts.ALGORITHM_REQUIREMENTS:
            requirements = PathConcepts.ALGORITHM_REQUIREMENTS[algo]
            should_include = True

            # check intent compatibility
            if requirements["required_intents"] and not (
                requirements["required_intents"] & path_intents
            ):
                should_include = False
                exclusion_reasons[algo].add("incompatible with query intent")

            # check source/target reqs
            if should_include:
                if requirements.get("requires_source") and not has_source:
                    should_include = False
                    exclusion_reasons[algo].add("missing source")
                if requirements.get("requires_target") and not has_target:
                    should_include = False
                    exclusion_reasons[algo].add("missing target")

            if should_include:
                filtered_algorithms.append(algo)
            else:
                logger.info(
                    f"Excluding algorithm '{algo}' due to "
                    f"{' and '.join(exclusion_reasons[algo])}."
                )
        else:
            # for non-path algorithms, include them without filtering
            filtered_algorithms.append(algo)

    return filtered_algorithms
