from django import forms
from tasks.models import Task,TaskDetail
# django form (naive approach)

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250,label="task title")
    description = forms.CharField(widget=forms.Textarea,label="task description")
    due_date = forms.DateField(widget=forms.SelectDateWidget,label="due date")
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],label="assigned to")
    
    
    
    def __init__(self,*args,**kargs): # (* and **) diye unpacked kore data pataitasi
        #print(args,kargs)
        employ = kargs.pop("employees",[]) #view theke kargs patassi ata catch korce
        super().__init__(*args,**kargs)
        self.fields['assigned_to'].choices = [
            (emp.id ,emp.name) for emp in employ
        ]

class StyleformedMixing:
    """mixing to appy to form field"""
    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)
        self.apply_styled_widgets()
    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:border-rose-500 focus:outline-none focus:ring-rose-500"
    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder' : f"Enter {field.label.lower()}",
                    'rows':5
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class":"border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:border-rose-500 focus:outline-none focus:ring-rose-500"
                    
                })  
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"space-y-2"
                })  
            else:
                field.widget.attrs.update({
                    'class':self.default_classes,
                }) 



# Django Model form

class TaskModelform(StyleformedMixing,forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','assigned_to','due_date']
        widgets ={
            'due_date':forms.SelectDateWidget,
            'assigned_to':forms.CheckboxSelectMultiple
        }
        
        #fields = '__all__'
        #exclude = ['project','title']
        # widgets = {
        #     'title' : forms.TextInput(attrs={
        #         'class':"border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
        #         'placeholder':"Enter task title"
        #         }),
        #     'description' : forms.Textarea(attrs={
        #         'class':"border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
        #         'placeholder':"Enter task details..........",
        #         'rows':5,
        #         }),
        #     'due_date' : forms.SelectDateWidget(attrs={
        #         'class':"border-2 border-gray-300 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
        #         }),
        #     'assigned_to' : forms.CheckboxSelectMultiple()
        # }
        
class TaskDetailForm(StyleformedMixing,forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority','notes']
        
   