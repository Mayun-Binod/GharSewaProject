import mongoose from 'mongoose'
import bcrypt from 'bcryptjs'
import validator from 'validator'

const userSchema = mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      validate: [
        {
          validator: function (value) {
            return value.length >= 2;
          },
          message: 'Name must be at least 2 characters long',
        },
        {
          validator: function (value) {
            return /^[^0-9]*$/.test(value);
          },
          message: 'Name must not contain any numbers',
        },
      ],
    },
    email: {
      type: String,
      required: true,
      unique: true,
    },
    password: {
      type: String,
      required: true,
      // validate: [
      //   {
      //     validator: function (value) {
      //       return value.length >= 6;
      //     },
      //     message: 'Password must be at least 6 characters long',
      //   },
      //   {
      //     validator: function (value) {
      //       return /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$/.test(
      //         value
      //       );
      //     },
      //     message:
      //       'Password must contain at least one capital letter, one number, and one symbol',
      //   },
      // ],
    },
    isAdmin: {
      type: Boolean,
      required: true,
      default: false,
    },
  },
  {
    timestamps: true,
  }
);

userSchema.methods.matchPassword = async function (enteredPassword) {
  return await bcrypt.compare(enteredPassword, this.password)
}

userSchema.pre('save', async function (next) {
  if (!this.isModified('password')) {
    next()
  }

  const salt = await bcrypt.genSalt(10)
  this.password = await bcrypt.hash(this.password, salt)
})

const User = mongoose.model('User', userSchema)

export default User
