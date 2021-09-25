const { Sequelize, DataTypes } = require('sequelize')
const sequelize = new Sequelize('sqlite:///home/salism3/projects/jadiinbot/db.sqlite3')

// const User = sequelize.define('main_user', {
//     id: {
//         type: DataTypes.INTEGER,
//         allowNull: false,
//         primaryKey: true,
//         autoIncrement: true,
//     },
//     password: {
//         type: DataTypes.STRING,
//         allowNull: false,
//     },
//     last_login: {
//         type: DataTypes.DATE,
//     },
//     is_superuser: {
//         type: DataTypes.BOOLEAN,
//         allowNull: false,
//     },
//     username: {
//         type: DataTypes.STRING,
//         allowNull: false,
//         unique: true,
//     },
//     first_name: {
//         type: DataTypes.STRING,
//         allowNull: false,
//     },
//     last_name: {
//         type: DataTypes.STRING,
//         allowNull: false,
//     },
//     email: {
//         type: DataTypes.STRING,
//         allowNull: false,
//     },
//     is_staff: {
//         type: DataTypes.BOOLEAN,
//         allowNull: false,
//     },
//     is_active: {
//         type: DataTypes.BOOLEAN,
//         allowNull: false,
//     },
//     date_joined: {
//         type: DataTypes.DATE,
//         allowNull: false,
//     }

// }, {
//     timestamps: false,
//     createdAt: false,
//     updatedAt: false,
//     freezeTableName: true
// })


const Session = sequelize.define('main_session', {
    id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        primaryKey: true,
        autoIncrement: true,
    },
    session: {
        type: DataTypes.TEXT,
        allowNull: false,
    },
    owner_id: {
        type: DataTypes.BIGINT,
        allowNull: false,
        unique: true,
    }
}, {
    timestamps: false,
    createdAt: false,
    updatedAt: false,
    freezeTableName: true
})

// Session.belongsTo(User, {
//     foreignKey: 'id',
// })

module.exports = {
    Session
}