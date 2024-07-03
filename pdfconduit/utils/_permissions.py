class Permissions:
    def __init__(self, pdf):
        self._permissions = pdf.user_access_permissions.to_dict()

    def all(self):
        return self._permissions

    def can(self, permission):
        return permission in self._permissions and self._permissions[permission]

    def can_print(self):
        return self.can("print")

    def can_modify(self):
        return self.can("modify")

    def can_copy(self):
        return self.can("copy")

    def can_annotate(self):
        return self.can("annotations")

    def can_fill_forms(self):
        return self.can("forms")

    def can_change_accessability(self):
        return self.can("accessability")

    def can_assemble(self):
        return self.can("assemble")

    def can_print_high_quality(self):
        return self.can("print_high_quality")
