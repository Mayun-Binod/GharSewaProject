import asyncHandler from 'express-async-handler'
import Product from '../models/productModel.js'
import Order from "../models/orderModel.js"
import User from "../models/userModel.js"

// @desc    Fetch all products
// @route   GET /api/products
// @access  Public
const getProducts = asyncHandler(async (req, res) => {
  const pageSize = 10;
  const page = Number(req.query.pageNumber) || 1;

  const keyword = req.query.keyword
    ? {
        name: {
          $regex: req.query.keyword,
          $options: 'i',
        },
      }
    : {};

  const count = await Product.countDocuments({ ...keyword });
  const products = await Product.find({ ...keyword })
    .limit(pageSize)
    .skip(pageSize * (page - 1));

  // Apply Merge Sort to sort the products array based on name in ascending order
  const sortedProducts = mergeSort(products, 'name');

  res.json({ products: sortedProducts, page, pages: Math.ceil(count / pageSize) });
});

// Merge Sort function
function mergeSort(arr, sortBy) {
  if (arr.length <= 1) {
    return arr; // Base case: array with 0 or 1 element is already sorted
  }

  // Split the array into two halves
  const middle = Math.floor(arr.length / 2);
  const leftHalf = arr.slice(0, middle);
  const rightHalf = arr.slice(middle);

  // Recursively call mergeSort on the left and right halves
  const sortedLeft = mergeSort(leftHalf, sortBy);
  const sortedRight = mergeSort(rightHalf, sortBy);

  // Merge the sorted left and right halves
  return merge(sortedLeft, sortedRight, sortBy);
}

// Merge function
function merge(leftArr, rightArr, sortBy) {
  let sortedArr = [];
  let leftIdx = 0;
  let rightIdx = 0;

  // Compare elements from left and right arrays and place them in sorted order
  while (leftIdx < leftArr.length && rightIdx < rightArr.length) {
    if (leftArr[leftIdx][sortBy] <= rightArr[rightIdx][sortBy]) {
      sortedArr.push(leftArr[leftIdx]);
      leftIdx++;
    } else {
      sortedArr.push(rightArr[rightIdx]);
      rightIdx++;
    }
  }

  // Add remaining elements from left or right array
  while (leftIdx < leftArr.length) {
    sortedArr.push(leftArr[leftIdx]);
    leftIdx++;
  }

  while (rightIdx < rightArr.length) {
    sortedArr.push(rightArr[rightIdx]);
    rightIdx++;
  }

  return sortedArr;
}

// @desc    Fetch single product
// @route   GET /api/products/:id
// @access  Public
const getProductById = asyncHandler(async (req, res) => {
  const product = await Product.findById(req.params.id)

  if (product) {
    res.json(product)
  } else {
    res.status(404)
    throw new Error('Product not found')
  }
})

// @desc    Delete a product
// @route   DELETE /api/products/:id
// @access  Private/Admin
const deleteProduct = asyncHandler(async (req, res) => {
  const product = await Product.findById(req.params.id)

  if (product) {
    await product.remove()
    res.json({ message: 'Product removed' })
  } else {
    res.status(404)
    throw new Error('Product not found')
  }
})

// @desc    Create a product
// @route   POST /api/products
// @access  Private/Admin
const createProduct = asyncHandler(async (req, res) => {
  const product = new Product({
    name: 'Sample name',
    price: 0,
    user: req.user._id,
    image: '/images/sample.jpg',
    brand: 'Sample brand',
    category: 'Sample category',
    countInStock: 0,
    numReviews: 0,
    description: 'Sample description',
  })

  const createdProduct = await product.save()
  res.status(201).json(createdProduct)
})

// @desc    Update a product
// @route   PUT /api/products/:id
// @access  Private/Admin
const updateProduct = asyncHandler(async (req, res) => {
  const {
    name,
    price,
    description,
    image,
    brand,
    category,
    countInStock,
  } = req.body

  const product = await Product.findById(req.params.id)

  if (product) {
    product.name = name
    product.price = price
    product.description = description
    product.image = image
    product.brand = brand
    product.category = category
    product.countInStock = countInStock

    const updatedProduct = await product.save()
    res.json(updatedProduct)
  } else {
    res.status(404)
    throw new Error('Product not found')
  }
})

// @desc    Create new review
// @route   POST /api/products/:id/reviews
// @access  Private
const createProductReview = asyncHandler(async (req, res) => {
  const { rating, comment } = req.body

  const product = await Product.findById(req.params.id)

  if (product) {
    const alreadyReviewed = product.reviews.find(
      (r) => r.user.toString() === req.user._id.toString()
    )

    if (alreadyReviewed) {
      res.status(400)
      throw new Error('Product already reviewed')
    }

    const review = {
      name: req.user.name,
      rating: Number(rating),
      comment,
      user: req.user._id,
    }

    product.reviews.push(review)

    product.numReviews = product.reviews.length

    product.rating =
      product.reviews.reduce((acc, item) => item.rating + acc, 0) /
      product.reviews.length

    await product.save()
    res.status(201).json({ message: 'Review added' })
  } else {
    res.status(404)
    throw new Error('Product not found')
  }
})

// @desc    Get top rated products
// @route   GET /api/products/top
// @access  Public






//algorithm start



const findSimilarUsers = async (userId) => {
  console.log('Inside findSimilarUsers');
  const userhistry=[];
  const userOrders = await Order.find({ user: userId });
  for (const uorder of userOrders) {
    for (const uitem of uorder.orderItems) {
      userhistry.push(uitem.name)
    }
  }
  const otherUsers = await User.find({ _id: { $ne: userId } });
  console.log('userhistry:', userhistry);
  console.log('otherUsers:', otherUsers);

  const similarUsers = [];
  const disproduct=[]
  
  for (const otherUser of otherUsers) {
    let otherhistry=[];
    const otherUserOrders = await Order.find({ user: otherUser._id });
    for (const otheruser of otherUserOrders) {
      
      for (const otherItem of otheruser.orderItems) {
        otherhistry.push(otherItem.name)
      }
    }
    console.log('otherUserOrders:', otherhistry);

    const similarity = userhistry.filter((order) =>
    otherhistry.includes(order)).length;
    console.log("similar item",similarity);

    if (similarity > 1) {
      similarUsers.push({
        userId: otherUser._id,
        similarity,
      })
      
      const dissimilarity = otherhistry.filter((order) =>
      !userhistry.includes(order));
      console.log("dissimilar" ,dissimilarity);
      disproduct.push(dissimilarity);
      
    }
  }
  const finalprod= [];
  console.log(disproduct);
  for (const subArray of disproduct) {
    for (const disproduct of subArray) {
      finalprod.push(disproduct)
    }
  }
  console.log(finalprod);
  

  return finalprod;
};

//algorithm ends

const getTopProducts = asyncHandler(async (req, res) => {
  try {
    console.log('Inside getTopProducts');
    
    // Retrieve user ID from request, set to null if not available
    const userId = req.user ? req.user._id : null;
    console.log('userId:', userId);

    // Find similar users based on the provided user ID
    const similarUsers = await findSimilarUsers(userId);
    console.log('similarUsers:', similarUsers);

    let products;

    if (similarUsers.length > 0) {
      // If there are similar users, aggregate products based on their preferences
      products = await Product.aggregate([
        {
          $match: {
            name: { $in: similarUsers }, // Match products with names in similarUsers array
          },
        },
        {
          $sort: {
            rating: -1, // Sort by rating in descending order
            price: 1,   // Then sort by price in ascending order
          },
        },
        {
          $group: {
            _id: '$name',         // Group by product name
            product: { $first: '$$ROOT' }, // Select the first document for each product name
          },
        },
        {
          $replaceRoot: { newRoot: '$product' }, // Replace the root with the selected documents
        },
        {
          $limit: 5, // Limit the results to the top 5 products
        },
      ]);
    } else {
      // If there are no similar users, simply fetch top products based on rating
      products = await Product.aggregate([
        {
          $sort: {
            rating: -1, // Sort by rating in descending order
            price: 1,   // Then sort by price in ascending order
          },
        },
        {
          $limit: 5, // Limit the results to the top 5 products
        },
      ]);
    }

    console.log('products:', products);

    // Send the top products as a JSON response
    res.json(products);
  } catch (error) {
    console.log('Error:', error);
    res.status(500).json({ error: 'Server Error' }); // Send 500 status and error message in case of error
  }
});








export {
  getProducts,
  getProductById,
  deleteProduct,
  createProduct,
  updateProduct,
  createProductReview,
  getTopProducts,
}
