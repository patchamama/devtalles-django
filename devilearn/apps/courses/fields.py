from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    # This method is called when the model instance is saved to the database. Before the instance is saved, this method checks 
    # if the field's value is None. If it is, the method calculates the next order value based on the highest existing value 
    # in the database, optionally filtered by other fields specified in for_fields. If no existing instances are found,
    # it sets the value to 0. Finally, it assigns this value to the model instance before saving.
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self.model.objects.all()

                if self.for_fields:
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }

                    qs = qs.filter(**query)

                last_item = qs.latest(self.attname)
                value = getattr(last_item, self.attname) + 1
            except ObjectDoesNotExist:
                value = 0

            setattr(model_instance, self.attname, value)

            return value
        else:
            return super().pre_save(model_instance, add)