from django.shortcuts import render
from django.views.generic import ListView, DeleteView, View
from roombook.models import Booking
from django.contrib import messages
from django.shortcuts import redirect, reverse
from datetime import date
from django.shortcuts import get_object_or_404
from forms.forms import CancelConfirmForm, ExtendBookingForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from booking_code.check_availability import check_extendability


class ShowDetails(ListView):
    
    template_name = "myaccount/myaccount.html"
    model = Booking
    context_object_name = 'mybookings'

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user, is_active=True)
 

class CancelBooking(SuccessMessageMixin, DeleteView):
    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        return Booking.objects.filter(
            pk=pk)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CancelBooking, self).delete(request, *args, **kwargs)
       

    model = Booking
    template_name= "myaccount/cancel_booking.html"
    form_class = CancelConfirmForm
    success_url = reverse_lazy("home:home")
    success_message  = "The booking has been canceled"
    

   

    def get(self, request, *args, **kwargs):
        bookid = self.kwargs.get('pk', None)
        today = date.today()
        booking = get_object_or_404(Booking, pk=bookid)
        checkin = booking.check_in
        print((checkin - today).days)
        if (checkin - today).days > 7:
            return render(request, self.template_name, {'booking':booking})
        elif (checkin - today).days < 7:
            messages.warning(request, 'Sorry! Cancelation only possible if checkin date is more than 7 days away')
            return redirect(reverse('myaccount:myaccount'))
        elif (checkin < today):
             messages.warning(request, 'Sorry! Checkin date has passed')
             return redirect(reverse('myaccount:myaccount'))
        else:
            return redirect(reverse('myaccount:myaccount'))



class ExtendBooking(View):
    
    # model =Booking
    # fields = [ 'check_out']
    template_name = 'myaccount/extend_booking.html'
    # success_url = reverse_lazy("home:home")
    
    
    def get(self, request, *args, **kwargs):
        form = ExtendBookingForm()
        bookid = type = self.kwargs.get('pk', None)
        bookid = get_object_or_404(Booking, pk=bookid)
    
        context = {
            'bookid': bookid,
            'form': form
        }

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        bookid = type = self.kwargs.get('pk', None)
        bookid = get_object_or_404(Booking, pk=bookid)
        form = ExtendBookingForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
        else:
            messages.warning(request, 'Form not valid')
            return redirect( reverse('myaccount:myaccount'))
        print(kwargs)
        print(data)

        if check_extendability(bookid.room_number, bookid.check_out, data['check_out']):
            co = data['check_out']
            bookid.check_out =  co
            bookid.save()
            # bookid.save(update_fields=["check_out"=data['check_out']) 
            messages.success(request, f"Thank you for extending room { bookid.room_number } to { data['check_out'] }")
            return redirect(reverse('home:home'))
        else:
            messages.warning(request, "Sorry that room is not available for those dates, try another room")
            return redirect(reverse('home:home'))
    #     def form_valid(self, form):
    #         instance = form.save(commit=False)
    #         instance.check_out = self.request.check_out
    #         super(ExtendBooking(), self).save(form)


    #     bookid = type = self.kwargs.get('pk', None)
    #     bookid = get_object_or_404(Booking, pk=bookid)
        
    #     if check_availability(bookid.room_number, bookid.check_out, bookid.check_out):
    #         pass

        # return redirect(reverse('myaccount:myaccount'))