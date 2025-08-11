from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            'ix': 'ix_%(column_0_label)s',
            'uq': 'uq_%(table_name)s_%(column_0_name)s',
            'ck': 'ck_%(table_name)s_%(constraint_name)s',
            'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
            'pk': 'pk_%(table_name)s',
        }
    )


# class OrganizationCategory(Base):
#     __tablename__ = 'organization_category'
#     __table_args__ = (UniqueConstraint('organization_id', 'category_id'),)

#     organization_id: Mapped[int] = mapped_column(
#         ForeignKey('organizations.id', ondelete='CASCADE'), primary_key=True
#     )
#     category_id: Mapped[int] = mapped_column(
#         ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True
#     )

organization_category = Table(
    'organization_category',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True),
)

class Organization(Base):
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    phone_numbers: Mapped[list['PhoneNumber']] = relationship(back_populates='organization')

    building_id: Mapped[int] = mapped_column(ForeignKey('buildings.id'))
    building: Mapped['Building'] = relationship(back_populates='organizations')

    categories: Mapped[list['Category']] = relationship(
        secondary=organization_category,
        back_populates='organizations',
    )


class PhoneNumber(Base):
    __tablename__ = 'phone_numbers'
    
    id: Mapped[int] = mapped_column(primary_key=True)

    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))
    organization: Mapped['Organization'] = relationship(back_populates='phone_numbers')

class Building(Base):
    __tablename__ = 'buildings'

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(255))
    coordinates: Mapped[str] = mapped_column(String(50))  # TODO separate Float attributes

    organizations: Mapped[list['Organization']] = relationship(back_populates='building')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    parent_id: Mapped[int | None] = mapped_column(ForeignKey('categories.id'), nullable=True)
    parent: Mapped['Category'] = relationship(back_populates='children', remote_side=lambda: Category.id)
    children: Mapped[list['Category']] = relationship(back_populates='parent')

    organizations: Mapped[list['Organization']] = relationship(
        secondary=organization_category,
        back_populates='categories',
    )

