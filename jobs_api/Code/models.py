from dataclasses import dataclass, field, asdict
from typing import List, Optional, Any, Dict


@dataclass
class Job:
    # normalized id (from MongoDB's {"_id": {"$oid": "..."}})
    id: Optional[str] = None

    job_id: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    location: List[str] = field(default_factory=list)
    employment_type: Optional[str] = None
    salary: Optional[str] = None
    experience: Optional[str] = None
    url: Optional[str] = None

    # text fields that in your example are lists of strings
    description: List[str] = field(default_factory=list)
    qualifications: List[str] = field(default_factory=list)
    summarized_description: List[str] = field(default_factory=list)
    summarized_qualifications: List[str] = field(default_factory=list)

    status: Optional[str] = None

    @classmethod
    def from_mongo(cls, doc: Dict[str, Any]) -> "Job":
        """
        Create a Job dataclass from a MongoDB document (possibly using Mongo's extended JSON)
        - Ignores 'timestamps' key entirely
        - Normalizes _id to a simple string (if in {"$oid": "..."} format)
        - Ensures list fields are lists
        """
        # defensive shallow copy so we don't mutate the original
        d = dict(doc)

        # Normalize id
        _id = d.get("_id")
        normalized_id = None
        if isinstance(_id, dict):
            # common pattern: {"$oid": "<hex>"} or {"$oid": {"$numberLong": "..."}}
            if "$oid" in _id:
                normalized_id = _id["$oid"]
            elif "$binary" in _id:  # just in case different representation
                normalized_id = str(_id["$binary"])
            else:
                # fallback: try to stringify dict
                normalized_id = str(_id)
        elif _id is not None:
            normalized_id = str(_id)

        # Remove Mongo-specific fields we don't want
        d.pop("_id", None)
        d.pop("timestamps", None)  # explicitly ignore timestamps

        # Safely extract list fields (some docs may use empty string instead of list)
        def as_list(x):
            if x is None:
                return []
            if isinstance(x, list):
                return x
            # if stored as single string, convert to single-item list
            if isinstance(x, str):
                return [x] if x.strip() != "" else []
            # other iterable-like but not list
            try:
                return list(x)
            except Exception:
                return []

        job = cls(
            id=normalized_id,
            job_id=d.get("job_id"),
            company=d.get("company"),
            title=d.get("title"),
            location=as_list(d.get("location")),
            employment_type=d.get("employment_type") or None,
            salary=d.get("salary") or None,
            experience=d.get("experience") or None,
            url=d.get("url") or None,
            description=as_list(d.get("description")),
            qualifications=as_list(d.get("qualifications")),
            summarized_description=as_list(d.get("summarized_description")),
            summarized_qualifications=as_list(d.get("summarized_qualifications")),
            status=d.get("status") or None,
        )

        return job

    def to_dict(self, include_none: bool = False) -> Dict[str, Any]:
        """
        Convert dataclass back to dict. By default includes keys with None values;
        set include_none=False to drop None values.
        """
        d = asdict(self)
        if not include_none:
            d = {k: v for k, v in d.items() if v is not None}
        return d
