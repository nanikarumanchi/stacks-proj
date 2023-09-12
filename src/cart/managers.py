from django.db import models


class CartManager(models.Manager):
    def new_or_get(self, request):
        is_cart_created = False
        cart_id = request.session.get('cart_id', None)
        if cart_id is None:

            if request.user.is_authenticated:
                try:
                    cart_obj, is_new = self.get_cart_obj(
                        request.user)  # todo  self.get_queryset().get(user=request.user)

                    cart_id = cart_obj.id
                    is_cart_created = is_new
                    # print('user logged in no cart id is there check for cart for user. cart is there', cart_id)
                except:
                    cart_obj = self.create(user=request.user)
                    cart_id = cart_obj.id
                    # print('user logged in no cart id no cart for user. cart is created', cart_id)
                    is_cart_created = True
            else:
                cart_obj = self.create(user=None)
                cart_id = cart_obj.id
                # print('user not logged in, no cart id. cart created with empty user', cart_id)
        else:
            if request.user.is_authenticated:

                # # print('existing cart id', existing_cart_obj.id, 'cart user', existing_cart_obj.user)
                try:
                    cart_obj, is_new = self.get_cart_obj(request.user)
                    # todo self.get_queryset().get(user=request.user)
                    is_cart_created = is_new
                    # print('user logged in, cart id is there, check for user has cart or not? user have cart..')
                except self.model.DoesNotExist:
                    cart_obj = self.create(user=request.user)
                    # print('user logged in, cart id is there, no cart for user, create cart')
                    is_cart_created = True

                if self.get_queryset().filter(id=cart_id).exists():
                    existing_cart_obj = self.get_queryset().get(id=cart_id)
                    existing_cart_obj_order_qs = existing_cart_obj.cart_have_order()
                    if not existing_cart_obj_order_qs:
                        if existing_cart_obj.user is None:  # TODO check if it has billing profile or not
                            for product in existing_cart_obj.products.all():
                                if product not in cart_obj.products.all():
                                    cart_obj.products.add(product)
                            cart_obj.save()
                            existing_cart_obj.delete()
                            # print('existing cart doesnt have user')
                    else:
                        print('existing object have order with billing')
                cart_id = cart_obj.id
            else:
                cart_obj, is_cart_created = self.get_cart_obj(user=None)
                cart_id = cart_obj.id
                # print('cart exists user not logged in placing same cart', cart_id)
        request.session['cart_id'] = cart_id

        # print('session cart id', request.session.get('cart_id'))
        return cart_obj, is_cart_created

    def get_cart_obj(self, user):
        try:
            cart_temp_obj, is_new = self.model.objects.get_or_create(user=user)
        except:
            cart_temp_obj = self.get_queryset().filter(user=user).last()
            is_new = False
        cart_obj_with_order = cart_temp_obj.order_set.filter(cart=cart_temp_obj)
        if cart_obj_with_order.exists():
            cart_order_obj = cart_obj_with_order.first()
            if cart_order_obj.status == 'created':
                cart_obj = cart_temp_obj
                # print(cart_order_obj.status)
            else:
                cart_obj = self.model.create(user=user)
                is_new = True
        else:
            cart_obj = cart_temp_obj

        return cart_obj, is_new
