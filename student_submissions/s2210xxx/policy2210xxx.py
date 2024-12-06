from policy import Policy


class Policy2210xxx(Policy):
    def __init__(self):
        # Student code here
        pass

    # First Fit Decreasing    
    def get_action(self, observation, info):
        # Student code here
        list_prods = observation["products"]

        prod_size = [0, 0]
        stock_idx = -1
        pos_x, pos_y = 0, 0

        sorted_prods = sorted(list_prods, key=lambda x: x["size"][0] * x["size"][1], reverse=True)
        sorted_stock_incidies = self.sort_stock(observation)

        for prod in sorted_prods:
            if prod["quantity"] > 0:
                prod_size = prod["size"]

                for i in range (len(sorted_stock_incidies)):
                    stock = observation["stocks"][sorted_stock_incidies[i]]
                    stock_w, stock_h = self._get_stock_size_(stock)
                    prod_w, prod_h = prod_size

                    if stock_w >= prod_w and stock_h >= prod_h:
                        pos_x, pos_y = None, None
                        for x in range(stock_w - prod_w + 1):
                            for y in range(stock_h - prod_h + 1):
                                if self._can_place_(stock, (x, y), prod_size):
                                    pos_x, pos_y = x, y
                                    break
                            if pos_x is not None and pos_y is not None:
                                break

                        if pos_x is not None and pos_y is not None:
                            stock_idx = sorted_stock_incidies[i]
                            break

                    # if stock cannot fit the product, try to rotate the product
                    if stock_w >= prod_h and stock_h >= prod_w:
                        pos_x, pos_y = None, None
                        for x in range(stock_w - prod_h + 1):
                            for y in range(stock_h - prod_w + 1):
                                if self._can_place_(stock, (x, y), prod_size[::-1]):
                                    prod_size = prod_size[::-1]
                                    pos_x, pos_y = x, y
                                    break
                            if pos_x is not None and pos_y is not None:
                                break
                        if pos_x is not None and pos_y is not None:
                            stock_idx = sorted_stock_incidies[i]
                            break

                if pos_x is not None and pos_y is not None:
                    break

        return {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}

    # Student code here
    # You can add more functions if needed

    def area(self, stock1):
        stock1_w, stock1_h = self._get_stock_size_(stock1)

        return stock1_w * stock1_h

    def sort_stock(self, observation):
        sorted_stock_incidies = [i for i in range(len(observation["stocks"]))]
        sorted_stock_incidies = sorted(sorted_stock_incidies, key=lambda x: self.area(observation["stocks"][x]), reverse=True)
        return sorted_stock_incidies
