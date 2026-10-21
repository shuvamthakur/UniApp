class Subject:
    """Represents a subject a student can enrol in."""

    def __init__(self, id, mark=None, grade=None):
        self.id = str(id).zfill(3)
        self.mark = mark
        self.grade = grade

    def __str__(self):
        return f"Subject-{self.id}"

    def __repr__(self):
        return f"Subject(id={self.id!r}, mark={self.mark!r}, grade={self.grade!r})"
