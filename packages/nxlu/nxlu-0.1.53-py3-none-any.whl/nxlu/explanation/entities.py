import logging
import re
import warnings

from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

warnings.filterwarnings("ignore")

logger = logging.getLogger("nxlu")


__all__ = ["EntityExtractor"]


class EntityExtractor:
    """A class to manage loading and using the BERT model for entity extraction."""

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
        self.model = AutoModelForTokenClassification.from_pretrained(
            "dslim/bert-base-NER", ignore_mismatched_sizes=True
        )
        self.ner_pipeline = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple",
            device=-1,
        )

    def extract_entities(self, query: str, indicators: set[str]) -> list[str]:
        """Extract entities based on the indicators using the bert-base NER model.

        Parameters
        ----------
        query : str
            The user's input query string to analyze.
        indicators : Set[str]
            Set of indicator keywords relevant to the extraction process.

        Returns
        -------
        List[str]
            List of identified entities matching the provided indicators.
        """
        ner_results = self.ner_pipeline(query)

        # build a list of entities
        entities = [
            {
                "text": entity["word"],
                "type": entity["entity_group"],
                "start": entity["start"],
                "end": entity["end"],
            }
            for entity in ner_results
        ]

        # get positions of indicators in query
        indicators_positions = [
            {"indicator": indicator, "start": match.start(), "end": match.end()}
            for indicator in indicators
            for match in re.finditer(
                r"\b" + re.escape(indicator) + r"\b", query.lower()
            )
        ]

        # for each indicator position, find the entity that immediately proceeds it
        extracted_entities = []
        for ind_pos in indicators_positions:
            ind_end = ind_pos["end"]
            for entity in entities:
                if entity["start"] >= ind_end:
                    extracted_entities.append(entity["text"])
                    break

        return list(set(extracted_entities))

    def extract_all_entities(self, query: str) -> list[str]:
        """Extract all entities from the query using the NER model.

        Parameters
        ----------
        query : str
            The user's input query string to analyze.

        Returns
        -------
        List[str]
            List of identified entities.
        """
        ner_results = self.ner_pipeline(query)
        return list({entity["word"] for entity in ner_results})
