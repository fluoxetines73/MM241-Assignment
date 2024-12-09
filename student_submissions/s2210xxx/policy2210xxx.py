from policy import Policy
import numpy as np
import copy

# 1: Column Generation, 2: Branch and Bound, 3: First Fit Decreasing
class Policy2210xxx(Policy):
    def __init__(self, policy_id=1):
        assert policy_id in [1, 2, 3, 4], "Policy ID must be 1 or 2 or 3"

        self.policy_id = policy_id 
        # parameters for branch and bound
        self.best_action = []
        self.best_filled = int(1e9)
        self.root = None

    def get_action(self, observation, info):
        if self.policy_id == 1:
            # Column Generation
            return self.column_generation_action(observation, info)
        elif self.policy_id == 2:
            # Branch and Bound
            return self.branch_and_bound_action(observation, info)
        elif self.policy_id == 3:
            # First Fit Decreasing
            return self.first_fit_decreasing_action(observation, info)
        elif self.policy_id == 4:
            return self.first_fit_decreasing_action_2(observation, info)
        
    class Node:
        pass

    ############################################################################################################
    # First Fit Decreasing    
    def first_fit_decreasing_action(self, observation, info):
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

                for i in sorted_stock_incidies:
                    stock = observation["stocks"][i]
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
                            stock_idx = i
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
                            stock_idx = i
                            break

                if pos_x is not None and pos_y is not None:
                    break

        return {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}

    def area(self, stock1):
        stock1_w, stock1_h = self._get_stock_size_(stock1)

        return stock1_w * stock1_h

    def sort_stock(self, observation):
        sorted_stock_incidies = [i for i in range(len(observation["stocks"]))]
        sorted_stock_incidies = sorted(sorted_stock_incidies, key=lambda x: self.area(observation["stocks"][x]), reverse=True)
        return sorted_stock_incidies
   
    ############################################################################################################
    # branch and bound
    def branch_and_bound_action(self, observation, info):
        # initialize base value
        self.best_action = []

        self.root = Node(observation, info, [])
        node = self.root

        # use greedy policy to get base value
        terminated = False
        while (not terminated):
            action = self.first_fit_decreasing_action(node.observation, node.info)
            observation, terminated, info = self._step(action, node.observation, node.info)

            
    
    def _step(self, action, observation, info):
        stock_idx = action["stock_idx"]
        size = action["size"]
        position = action["position"]

        width, height = size
        x, y = position

        # Check if the product is in the product list
        product_idx = None
        for i, product in enumerate(observation["products"]):
            if np.array_equal(product["size"], size) or np.array_equal(
                product["size"], size[::-1]
            ):
                if product["quantity"] == 0:
                    continue

                product_idx = i  # Product index starts from 0
                break

        if product_idx is not None:
            # must make sure stock
            stock = observation["stocks"][stock_idx]
            # Check if the product fits in the stock
            stock_width = np.sum(np.any(stock != -2, axis=1))
            stock_height = np.sum(np.any(stock != -2, axis=0))
            if (
                x >= 0
                and y >= 0
                and x + width <= stock_width
                and y + height <= stock_height
            ):
                # Check if the position is empty
                if np.all(stock[x : x + width, y : y + height] == -1):
                    # self.cutted_stocks[stock_idx] = 1
                    stock[x : x + width, y : y + height] = product_idx
                    observation["products"][product_idx]["quantity"] -= 1

        # An episode is done iff the all product quantities are 0
        terminated = all([product["quantity"] == 0 for product in observation["products"]])
        # reward = 1 if terminated else 0  # Binary sparse rewards

        info = self._get_info(observation)

        return observation, terminated, info

    def _get_info(self, observation):
        cutted_stocks = [np.any(stock > 0) for stock in observation["stocks"]]

        filled_ratio = np.mean(cutted_stocks).item()
        trim_loss = []

        for sid, stock in enumerate(observation["stocks"]):
            if cutted_stocks[sid] == 0:
                continue
            tl = (stock == -1).sum() / (stock != -2).sum()
            trim_loss.append(tl)

        trim_loss = np.mean(trim_loss).item() if trim_loss else 1

        return {"filled_ratio": filled_ratio, "trim_loss": trim_loss}
    
    ############################################################################################################
    # Column Generation
    def column_generation_action(self, observation, info):
        # Student code here

        pass

class Node:
    def __init__(self, observation, info, actions):
        self.children = []
        self.observation = copy.deepcopy(observation)
        self.info = info
        self.actions = actions
        self.terminate = False
        self.truncate = False

    def generate_child(self):
        unfilled_products = [p for p in self.observation["products"] if p["quantity"] > 0]
        


# class Policy2210xxx(Policy):
#     def __init__(self):
#         self.best_action = None
#         self.best_bound = np.inf
#     def get_action(self, observation, info):
#         products = copy.deepcopy(observation["products"])
#         stocks = copy.deepcopy(observation["stocks"])

#         if isinstance(stocks, tuple):
#             stocks = list(stocks)

#         prod_idx, rotated = self._select_product(products)
#         if prod_idx is None:
#             return {"stock_idx": -1, "size": [0, 0], "position": (0, 0)}
        
#         prod_size = products[prod_idx]["size"]
#         if rotated:
#             prod_size = [prod_size[1], prod_size[0]] #xoay

#         products[prod_idx]["quantity"] -= 1

    
#         self.best_action = {"stock_idx": -1, "size": prod_size, "position": (0, 0)}
#         self.best_bound = np.inf

   
#         self._branch_and_bound(products, stocks, prod_idx, prod_size, [])

#         return self.best_action

#     def _branch_and_bound(self, products, stocks, prod_idx, prod_size, actions_taken):
       
#         for s_idx, stock in enumerate(stocks):
#             stock_w, stock_h = self._get_stock_size_(stock)
#             w, h = prod_size

#             if stock_w < w or stock_h < h:
#                 continue 

#             for x in range(stock_w - w + 1):
#                 for y in range(stock_h - h + 1):
#                     if self._can_place_(stock, (x, y), prod_size):
                    
#                         remaining_space = self._calculate_bound_(stock, (x, y), prod_size)

#                         if remaining_space >= self.best_bound:
#                             continue 
                     
#                         self.best_bound = remaining_space
#                         self.best_action = {
#                             "stock_idx": s_idx,
#                             "size": prod_size,
#                             "position": (x, y)
#                         }

                     
#                         if remaining_space == 0:
#                             return  

                  
#                         backup_stock = stocks[s_idx].copy()
#                         self._place_product(stocks[s_idx], (x, y), prod_size)
#                         actions_taken.append({
#                             "stock_idx": s_idx,
#                             "size": prod_size,
#                             "position": (x, y)
#                         })

                       
#                         next_prod_idx, next_rotated = self._select_product(products)
#                         if next_prod_idx is not None:
#                             next_prod_size = products[next_prod_idx]["size"]
#                             if next_rotated:
#                                 next_prod_size = [next_prod_size[1], next_prod_size[0]]
#                             products[next_prod_idx]["quantity"] -= 1
#                             self._branch_and_bound(products, stocks, next_prod_idx, next_prod_size, actions_taken)
#                             products[next_prod_idx]["quantity"] += 1  # back

                   
#                         stocks[s_idx] = backup_stock
#                         actions_taken.pop()

#     def _select_product(self, products):

#         sorted_products = sorted(
#             [(i, p["size"], p["quantity"]) for i, p in enumerate(products) if p["quantity"] > 0],
#             key=lambda x: x[1][0] * x[1][1],
#             reverse=True
#         )
#         for i, size, qty in sorted_products:
#             # Thử cả hai hướng: không xoay và xoay
#             for rotated in [False, True]:
#                 if rotated and size[0] == size[1]:
#                     continue  # Nếu width == height, không cần xoay
#                 return i, rotated
#         return None, False

#     def _calculate_bound_(self, stock, position, size):
    
#         x, y = position
#         w, h = size
#         stock_w, stock_h = self._get_stock_size_(stock)
#         remaining_space = (stock_w * stock_h) - (w * h)
#         return remaining_space

#     def _evaluate_solution(self, stocks):
       
#         ratios = []
#         for stock in stocks:
#             stock_w, stock_h = self._get_stock_size_(stock)
#             if stock_w == 0 or stock_h == 0:
#                 ratios.append(0)
#                 continue
#             filled = np.sum(stock != -1)
#             total = stock_w * stock_h
#             ratios.append(filled / total if total > 0 else 0)
#         return np.mean(ratios)

#     def _place_product(self, stock, position, size):
     
#         x, y = position
#         w, h = size
#         stock[x:x+w, y:y+h] = -1 