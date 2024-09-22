import bcrypt from 'bcryptjs'

const users = [
  {
    name: 'Admin User',
    email: 'admin@example.com',
    password: bcrypt.hashSync('123456', 10),
    isAdmin: true,
  },
  {
    name: 'sandip',
    email: 'sandip03@gmail.com',
    password: bcrypt.hashSync('12345', 10),
  },
  {
    name: 'sandesh',
    email: 'sandesh1@gmail.com',
    password: bcrypt.hashSync('123456', 10),
  },
]

export default users
