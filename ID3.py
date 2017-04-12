from node import Node
import math


debug = True

def mode(examples):
  value_1 = examples[0]['Class']
  value_2 = None
  count = 0
  base_count = 0
  for example in examples:
    if example['Class'] == value_1:
      count += 1
    else:
      if not value_2:
        value_2 = example['Class']
      count -= 1

  if count > 0:
    return value_1
  return value_2


def get_branches(examples, best_attribute):
  branch_1 = list()
  branch_2 = list()

  base_value = examples[0][best_attribute]
  for example in examples:
    value = example[best_attribute]
    del example[best_attribute]
    if value == base_value:
      branch_1.append(example)
    else:
      branch_2.append(example)
  return branch_1, branch_2

# classification_data - list of republicans and democrats
# return entropy on the data
def find_entropy(classification_data):
  total = len(classification_data)
  pos = len([i for i, x in enumerate(classification_data) if x == classification_data[0]])
  neg = total - pos
  try: 
    return -(float(pos)/float(total))*math.log((float(pos)/float(total)),2) - (float(neg)/float(total))*math.log((float(neg)/float(total)),2)
  except ValueError as e:
    # if we get here all the values are either all positive or all negative and the equation equates to 0
    print "Pos value is: ",pos
    print "total value is: ",total
    print e
    return 0
  except ZeroDivisionError as e:
    print "Pos value is: ", pos
    print "total value is: ", total
    print e 
    return 0

# given an attribute, compute its gain
def find_information_gain(attribute, examples, total_entropy):
  # will either be 'y' or 'n' with our data set
  base_value = examples[0][attribute]
  classification_data_set_1 = list()
  classification_data_set_2 = list()

  for example in examples:
    attribute_value = example[attribute]
    if attribute_value == base_value:
      classification_data_set_1.append(example['Class'])
    else:
      classification_data_set_2.append(example['Class'])

  set_1_weight = len(classification_data_set_1)/len(examples)
  set_2_weight = 1 - set_1_weight

  entropy_set_1 = find_entropy(classification_data_set_1)
  entropy_set_2 = find_entropy(classification_data_set_2)

  print "entropy 1 and entrppy 2 is", entropy_set_1, entropy_set_2

  return total_entropy - set_1_weight*entropy_set_1 - set_2_weight*entropy_set_2


# loop through attributes, find attribute with highest information gain and return it
def find_best_attribute(examples):
  attributes = examples[0].keys()
  # removes key: Class as it is not an attribute
  attributes.remove('Class')

  best_attribute = None
  max_gain = 0
  classification_data = [example['Class'] for example in examples]
  total_entropy = find_entropy(classification_data)

  for attribute in attributes:
    gain = find_information_gain(attribute, examples, total_entropy)
    if gain > max_gain:
      max_gain = gain
      best_attribute = attribute
  return best_attribute



# return False if not homogenous
# else return True
def is_homogenous(examples):
  base_class = examples[0]['Class']
  for example in examples:
    if example['Class'] != base_class:
      return False
  return True



def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  # create root node
  root_node = Node()
  # check if all classications are the same
  if is_homogenous(examples):
    root_node.label = examples[0]['Class']
    print "is_homogenous is returning true"
    return root_node
  # if no more attributes to split on, set the label or root_node to default
  elif len(examples[0]) == 1:
    print "returning default"
    root_node.label = default
    return root_node
  else:
    best_attribute = find_best_attribute(examples)
    root_node.label = best_attribute
    print "the best attribute found is ", best_attribute
    branch_1, branch_2 = get_branches(examples, best_attribute)
    root_node.branches.append(branch_1)
    root_node.branches.append(branch_2)
    for branch in root_node.branches:
      mode_branch = mode(branch)
      print "Mode_branch is ", mode_branch
      print "length of branch is", len(branch)
      if len(branch) == 0:
        leaf_node = Node()
        leaf_node.label = mode_branch
        print "creating a leaf node with mode value"
        if len(root_node.children) == 0:
          root_node.children[0] = leaf_node
          print "storing that leaf node in position 0"
        else:
          root_node.children[1] = leaf_node
          print "storing that leaf node in position 1"
      else:
        print "length of root node children list is ", len(root_node.children)
        if len(root_node.children) == 0: 
          root_node.children[0] = ID3(branch, mode_branch)
        else:
          root_node.children[1] = ID3(branch, mode_branch)


def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  count = 0
  for example in examples:
    if example['Class'] == evaluate(node, example):
      count += 1

  return count/len(examples)


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  while node.children:
    attribute = node.label
    if example[attribute] == node.branches[0][0][attribute]:
      node = node.children[0]
    else:
      node = node.children[1]
  return node.label



#
#
# TEST CASES 
#
#
def test_ID3():
  from parse import parse
  data = parse('house_votes_84.data')
  tree = ID3(data, 'Republican')
  print tree


def test_find_entropy():
  data = ['Republican', 'Democrat', 'Democrat', 'Democrat', 'Democrat', 'Democrat', 'Republican', 'Republican']
  val = -(float(3)/float(8))*(math.log((float(3)/float(8)),2)) - (float(5)/float(8))*(math.log((float(5)/float(8)),2))
  assert_val = find_entropy(data)
  assert(assert_val== val)
  print "Passed test: test_find_entropy()\n"
  

if debug:
  test_find_entropy()
  test_ID3()
  
