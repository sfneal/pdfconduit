from typing import Dict

from pypdf import PdfReader


class Permissions:
    def __init__(self, pdf: PdfReader):
        self._permissions = pdf.user_access_permissions.to_dict()

    def all(self) -> Dict[str, bool]:
        return self._permissions

    def can(self, permission: str) -> bool:
        return permission in self._permissions and self._permissions[permission]

    def can_print(self) -> bool:
        return self.can("print")

    def can_modify(self) -> bool:
        return self.can("modify")

    def can_copy(self) -> bool:
        return self.can("copy")

    def can_annotate(self) -> bool:
        return self.can("annotations")

    def can_fill_forms(self) -> bool:
        return self.can("forms")

    def can_change_accessability(self) -> bool:
        return self.can("accessability")

    def can_assemble(self) -> bool:
        return self.can("assemble")

    def can_print_high_quality(self) -> bool:
        return self.can("print_high_quality")
